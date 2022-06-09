# import all relevant packages
from ebcpy import TimeSeriesData
import pandas as pd
import math
import numpy as np


def heating_demand(zoneNumber):
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    HeatingDemand = ResultData.loc[:, "multizone.zone[" + str(zoneNumber) + "].PHeater"]
    return HeatingDemand


def t_room(zoneNumber):
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    T_Room = ResultData.loc[:, "multizone.TAir[" + str(zoneNumber) + "]"]
    return T_Room


def t_outside():
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    T_Outside = ResultData.loc[:, "weaDat.weaBus.TDryBul"]
    return T_Outside


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
    return T_Room_Set


def t_supply_lin(maxTSupply):
    TOutside = t_outside()

    Tilt = (294.15-maxTSupply)/(294.15-243.15)
    b = 294.15*(1-Tilt)
    tSupply = Tilt*TOutside+b

    return tSupply


def t_return_lin(maxTSupply):
    TOutside = t_outside()

    Tilt = (294.15-maxTSupply)/(294.15-243.15)
    b = 294.15*(1-Tilt)
    tReturn = Tilt*TOutside+b

    return tReturn


def total_zone():
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    ZoneNumber = ResultData.loc[:, "multizone.numZones"]

    return ZoneNumber

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


def supply_my_formula():
    # required variable
    tRoom = t_room(1)
    tOut = t_outside()
    tRoomNom = 294.15  # K
    tOutNom = t_outside_nom(68161)+273.15
    tLogNom = 48.9  # Recknagel, page 1296
    n = 1.3  # Recknagel

    # calculations
    c1 = math.e**(((((tRoom-tOut)/(tRoomNom-tOutNom))**(1-n))*((np.log(tLogNom))**(-n)))**-1)
    # c2 = hLol/(m*cp)
    c2 = 1
    tSupply = (c1*tRoom-tRoom+c1*c2*(tRoom-tOut))/(c1-1)

    return tSupply
