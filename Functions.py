# import all relevant packages
from ebcpy import TimeSeriesData
import pandas as pd
import math


def heating_demand(zoneNumber):
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    HeatingDemand = ResultData.loc[:, "multizone.zone[" + str(zoneNumber) + "].PHeater"]
    return HeatingDemand


def t_room(zoneNumber):
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    T_Room = ResultData.loc[:, "multizone.TAir[" + str(zoneNumber) + "]"]
    T_Room.columns = ["T_Room"]
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


def t_supply_lin(maxTSupply, minTSupply):
    TOutside = t_outside()

    Tilt = (294.15-maxTSupply)/(294.15-243.15)
    b = 294.15*(1-Tilt)
    tSupply = Tilt*TOutside+b

    return tSupply


def t_return_lin(maxTSupply, minTSupply):
    TOutside = t_outside()

    Tilt = (294.15-maxTSupply)/(294.15-243.15)
    b = 294.15*(1-Tilt)
    tReturn = Tilt*TOutside+b

    return tReturn


def total_zone():
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")
    ZoneNumber = ResultData.loc[:, "multizone.numZones"]

    return  ZoneNumber
