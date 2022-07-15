# import all relevant packages
from ebcpy import TimeSeriesData
import pandas as pd
import math
import numpy as np


def get_data(zone_number, name):
    ResultData = TimeSeriesData("D:/hkr-fme/Projects/Bachelorarbeit1/Results/results" + name + ".mat")
    Data = ResultData[["multizone.zone[" + str(zone_number) + "].PHeater", "multizone.TAir[" + str(zone_number) + "]",
                       "weaDat.weaBus.TDryBul"]]
    Data.columns = ["HeatingDemand", "TRoom", "TOutside"]
    return Data


def get_filtered_data(zone_number, name):
    ResultData = TimeSeriesData("D:/hkr-fme/Projects/Bachelorarbeit1/Results/results" + name + ".mat")
    Data = ResultData[["multizone.zone[" + str(zone_number) + "].PHeater", "multizone.TAir[" + str(zone_number) + "]",
                       "weaDat.weaBus.TDryBul"]]
    Data.columns = ["HeatingDemand", "TRoom", "TOutside"]
    copy = Data.copy()
    indexNames = copy[copy["TRoom"] >= 294.15].index
    copy.drop(indexNames, inplace=True)
    return copy


def t_outside_nom(PLZ):
    df = pd.read_excel('C:/Users/hkr-fme/Downloads/DIN_TS_12831-1_Klimadaten.xlsx')
    df_keys = list(df.keys())
    for ind in df.index:
        if df[df_keys[0]][ind] == PLZ:
            data = df[df_keys[2]][ind]
    return data


def t_room_set(zoneNumber, name):
    ResultData = TimeSeriesData("D:/hkr-fme/Projects/Bachelorarbeit1/Results/results" + name + ".mat")
    T_Room_Set = ResultData.loc[:, "multizone.zone[" + str(zoneNumber) + "].TSetHeat"]
    c = float(T_Room_Set.iloc[0]['raw'])
    return c


def t_supply_lin(maxTSupply, zone_number, name):
    FilteredData = get_filtered_data(zone_number, name)
    TOutside = FilteredData["TOutside"]
    TOutNom = get_t_air_nom(zone_number, name)
    Tilt = (294.15-(maxTSupply+273.15))/(294.15-TOutNom)
    b = 294.15*(1-Tilt)
    tSupply = Tilt*TOutside+b

    return tSupply


def t_return_lin(maxTSupply, zone_number, name):
    FilteredData = get_filtered_data(zone_number, name)
    TOutside = FilteredData["TOutside"]
    TOutNom = get_t_air_nom(zone_number, name)
    Tilt = (294.15-(maxTSupply+273.15))/(294.15-TOutNom)
    b = 294.15*(1-Tilt)
    tReturn = Tilt*TOutside+b

    return tReturn


def get_q_nom(name):
    ResultData = TimeSeriesData("D:/hkr-fme/Projects/Bachelorarbeit1/Results/results" + name + ".mat")
    qNom = ResultData.loc[:, "multizone.zoneParam[1].hHeat"]
    c = int(qNom.iloc[0]['raw'])

    return c


def total_zone(name):
    ResultData = TimeSeriesData("D:/hkr-fme/Projects/Bachelorarbeit1/Results/results" + name + ".mat")
    ZoneNumber = ResultData.loc[:, "multizone.numZones"]
    c = int(ZoneNumber.iloc[0]['raw'])

    return c


def supply_nom():
    # required variables
    tRoomNom = 293.15  # K, source--> Recknagel, page 1375
    tSupplyNom = 348.15  # K, source--> Recknagel, page 1375
    tReturnNom = 338.15  # K, source--> Recknagel, page 1375
    delta_T_log_nom = (tSupplyNom - tReturnNom) / np.log(
        (tSupplyNom - tRoomNom) / (tReturnNom - tRoomNom))  # source -->Supply Temperature Control Concepts, page 51
    tOutsideNom = t_outside_nom(68159) + 273.15  # enter PLZ of weather data, source --> DIN_TS 12831-1
    n = 1.3  # for radiator, source Recknagel, page 1375

    # calculate supply temperature, source --> Supply Temperature Control Concepts, page 53
    c1 = (tSupplyNom - tReturnNom) / (tRoomNom - tOutsideNom)
    c2 = (c1 * ((tRoomNom - tOutsideNom) ** (-1 / n))) / delta_T_log_nom
    delta_T_out = tRoomNom - tRoomNom
    # delta_T_out = tRoomNom - t_outside()
    c3 = math.e ** (c2 * (delta_T_out ** (1 - (1 / n))))
    tSupplyOper = (tRoomNom - c3 * (tRoomNom + c1 * delta_T_out)) / (1 - c3)

    return tSupplyOper


def supply_my_formula(zone_number, name):
    # required variable
    FilteredData = get_filtered_data(zone_number, name)
    tRoom = FilteredData["TRoom"]
    tOut = FilteredData["TOutside"]
    tRoomNom = 293.15  # K
    tOutNom = t_outside_nom(68161)+273.15
    tLogNom = 48.9  # Recknagel, page 1296
    n = 1.3  # Recknagel

    # calculations
    c1 = math.e**(((((tRoom-tOut)/(tRoomNom-tOutNom))**(1-n))*((np.log(tLogNom))**(-n)))**-1)
    # c2 = hTot/(m*cp)
    c2 = 0.33
    tSupply = (c1*tRoom-tRoom+c1*c2*(tRoom-tOut))/(c1-1)

    return tSupply


def get_t_lim(zone_number, name):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4
    Data = get_filtered_data(zone_number, name)
    tLim = Data["TOutside"].max()
    return tLim


def get_t_air_nom(zone_number, name):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4
    Data = get_filtered_data(zone_number, name)
    tAirNom = Data["TOutside"].min()
    return tAirNom


def t_supply_paper(zone_number, name, t_supply, t_return):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4

    # reqiured variables
    Data = get_filtered_data(zone_number, name)
    tLim = get_t_lim(zone_number, name)
    tAirNom = get_t_air_nom(zone_number, name)
    TRoom = Data["TRoom"]
    tOutside = Data["TOutside"]
    TSupplyNom = t_supply+273.15
    TReturnNom = t_return+273.15
    n = 1.3

    # calculations
    Q_rel = Data["HeatingDemand"]/get_q_nom(name)
    TSupply = TRoom + ((((TSupplyNom+TReturnNom)/2)-TRoom)*(Q_rel**(1/n))) + (((TSupplyNom-TReturnNom)/2)*Q_rel)

    return TSupply


def t_return_paper(zone_number, name, t_supply, t_return):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4

    # reqiured variables
    Data = get_filtered_data(zone_number, name)
    tLim = get_t_lim(zone_number, name)
    tAirNom = get_t_air_nom(zone_number, name)
    tOutside = Data["TOutside"]
    TSupply = t_supply_paper(zone_number, name, t_supply, t_return)
    TSupplyNom = t_supply + 273.15
    TReturnNom = t_return + 273.15

    # calulations
    Q_rel = Data["HeatingDemand"] / get_q_nom(name)
    TReturn = TSupply - Q_rel*(TSupplyNom-TReturnNom)

    return TReturn


def get_area (name):
    ResultData = TimeSeriesData("D:/hkr-fme/Projects/Bachelorarbeit1/Results/results" + name + ".mat")
    Area = ResultData.loc[:, "multizone.ABuilding"]
    c = int(Area.iloc[0]['raw'])

    return c


def optimal_t_supply(q_nom, spread, n, kA, t_room):
    c2 = spread/((q_nom/kA)**(1/n))
    c1 = math.e**c2
    t_supply = (-c1*(spread+t_room)+t_room)/(1-c1)
    return t_supply
