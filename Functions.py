# import all relevant packages
from ebcpy import TimeSeriesData
import pandas as pd
import math
import numpy as np


def get_data(zone_number):
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    Data = ResultData[["multizone.zone[" + str(zone_number) + "].PHeater", "multizone.TAir[" + str(zone_number) + "]",
                       "weaDat.weaBus.TDryBul"]]
    Data.columns = ["HeatingDemand", "TRoom", "TOutside"]
    return Data


def get_filtered_data(zone_number):
    x = pd.DataFrame()
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    Data = ResultData[["multizone.zone[" + str(zone_number) + "].PHeater", "multizone.TAir[" + str(zone_number) + "]",
                       "weaDat.weaBus.TDryBul"]]
    Data.columns = ["HeatingDemand", "TRoom", "TOutside"]
    indexNames = Data[Data["TRoom"] >= 294.15].index
    Data.drop(indexNames, inplace=True)
    return Data


def t_outside_nom(PLZ):
    df = pd.read_excel('C:/Users/hkr-fme/Downloads/DIN_TS_12831-1_Klimadaten.xlsx')
    df_keys = list(df.keys())
    for ind in df.index:
        if df[df_keys[0]][ind] == PLZ:
            data = df[df_keys[2]][ind]
    return data


def t_room_set(zoneNumber):
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    T_Room_Set = ResultData.loc[:, "multizone.zone[" + str(zoneNumber) + "].TSetHeat"]
    c = float(T_Room_Set.iloc[0]['raw'])
    return c


def t_supply_lin(maxTSupply, zone_number):
    FilteredData = get_filtered_data(zone_number)
    TOutside = FilteredData["TOutside"]
    Tilt = (294.15-maxTSupply)/(294.15-243.15)
    b = 294.15*(1-Tilt)
    tSupply = Tilt*TOutside+b

    return tSupply


def t_return_lin(maxTSupply, zone_number):
    FilteredData = get_filtered_data(zone_number)
    TOutside = FilteredData["TOutside"]
    Tilt = (294.15-maxTSupply)/(294.15-243.15)
    b = 294.15*(1-Tilt)
    tReturn = Tilt*TOutside+b

    return tReturn


def total_zone():
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
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


def supply_my_formula(zone_number):
    # required variable
    FilteredData = get_filtered_data(zone_number)
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


def get_t_lim(zone_number):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4
    Data = get_filtered_data(zone_number)
    tLim = Data["TOutside"].max()
    return tLim


def get_t_air_nom(zone_number):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4
    Data = get_filtered_data(zone_number)
    tAirNom = Data["TOutside"].min()
    return tAirNom


def t_supply_paper(zone_number):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4

    # reqiured variables
    Data = get_filtered_data(zone_number)
    tLim = get_t_lim(zone_number)
    tAirNom = get_t_air_nom(zone_number)
    TRoom = Data["TRoom"]
    tOutside = Data["TOutside"]
    TSupplyNom = 75+273.15
    TReturnNom = 65+273.15
    n = 1.3

    # calculations
    Q_rel = (tLim-tOutside)/(tLim-tAirNom)
    TSupply = TRoom + ((((TSupplyNom+TReturnNom)/2)-TRoom)*(Q_rel**(1/n))) + (((TSupplyNom-TReturnNom)/2)*Q_rel)

    return TSupply


def t_return_paper(zone_number):
    # source --> Performance of heat pumps retrofitted to radiator heating systems in
    # existing buildings and measures to reduce space heating temperatures, page 4

    # reqiured variables
    Data = get_filtered_data(zone_number)
    tLim = get_t_lim(zone_number)
    tAirNom = get_t_air_nom(zone_number)
    tOutside = Data["TOutside"]
    TSupply = t_supply_paper(zone_number)
    TSupplyNom = 75 + 273.15
    TReturnNom = 65 + 273.15

    # calulations
    Q_rel = (tLim - tOutside) / (tLim - tAirNom)
    TReturn = TSupply - Q_rel*(TSupplyNom-TReturnNom)

    return TReturn


