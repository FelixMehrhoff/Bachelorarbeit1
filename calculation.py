import Functions
import numpy as np
import pandas as pd
import CreateBuilding




def calculate_all_costs_lin(total_zone_number, name, t_supply, t_return):

    TotalCosts = 0
    TotalPower = 0
    AverageCOP = 0

    for i in range(1, total_zone_number+1):

        # requiredVariables
        electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom%C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20Strom%C2%ADkosten.
        t_supply_nom = t_supply
        t_return_nom = t_return
        FilteredData = Functions.get_filtered_data(i, name)
        tRoomSet = Functions.t_room_set(i, name)
        tOutside = FilteredData["TOutside"]
        heatingDemand = FilteredData["HeatingDemand"]
        tRoom = FilteredData["TRoom"]
        qualityGrade = 0.5

        # calculate tSupply and tReturn with linear solution
        # source --> https://www.viessmann.de/de/wohngebaeude/ratgeber/heizkurve-einstellen.html
        tSupply = Functions.t_supply_lin(t_supply_nom, i, name)
        tReturn = Functions.t_return_lin(t_return_nom, i, name)

        # get all parameters
        COP = (1/(1-tOutside/tSupply))*qualityGrade
        P_el = heatingDemand/COP
        costs = (electricityPrice/1000)*P_el  # divided by 1000, if electricity price is for kWh

        # put it in one dataframe
        data = pd.concat([COP, P_el, costs, tSupply, tReturn], axis=1, join='inner')
        data.columns = ["COP", "P_el", "costs", "tSupply", "tReturn"]

        # filter data not making sense (tSupply < tRoom)

        # sum up the costs
        zoneCosts = data['costs'].sum()
        TotalCosts += zoneCosts

        # sum up the power
        zonePower = data['P_el'].sum()
        TotalPower += zonePower

        # AverageCOP
        zoneCOP = data['COP'].sum()
        zoneAverageCOP = zoneCOP/len(data)
        AverageCOP += (zoneAverageCOP/total_zone_number)

    return (TotalCosts, TotalPower, AverageCOP)


def calculate_cop_lin(total_zone_number, name, t_supply, t_return):

    TotalCosts = 0
    TotalPower = 0
    AverageCOP = 0

    for i in range(1, total_zone_number+1):

        # requiredVariables
        electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom%C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20Strom%C2%ADkosten.
        tRoomNom = 293.15  # K, source--> Recknagel, page 1375
        t_supply_nom = t_supply
        t_return_nom = t_return
        FilteredData = Functions.get_filtered_data(i, name)
        tRoomSet = Functions.t_room_set(i, name)
        tOutside = FilteredData["TOutside"]
        heatingDemand = FilteredData["HeatingDemand"]
        tRoom = FilteredData["TRoom"]
        qualityGrade = 0.5

        # calculate tSupply and tReturn with linear solution
        # source --> https://www.viessmann.de/de/wohngebaeude/ratgeber/heizkurve-einstellen.html
        tSupply = Functions.t_supply_lin(t_supply_nom, i, name)
        tReturn = Functions.t_return_lin(t_return_nom, i, name)

        # get all parameters
        COP = (1/(1-tOutside/tSupply))*qualityGrade
        P_el = heatingDemand/COP
        costs = (electricityPrice/1000)*P_el  # divided by 1000, if electricity price is for kWh

        # put it in one dataframe
        data = pd.concat([COP, P_el, costs, tSupply, tReturn], axis=1, join='inner')
        data.columns = ["COP", "P_el", "costs", "tSupply", "tReturn"]

        # filter data not making sense (tSupply < tRoom)

        # sum up the costs
        zoneCosts = data['costs'].sum()
        TotalCosts += zoneCosts

        # sum up the power
        zonePower = data['P_el'].sum()
        TotalPower += zonePower

        # AverageCOP
        zoneCOP = data['COP'].sum()
        zoneAverageCOP = zoneCOP/len(data)
        AverageCOP += (zoneAverageCOP/total_zone_number)

    return AverageCOP


def calculate_total_power_lin(total_zone_number, name, t_supply, t_return):

    TotalCosts = 0
    TotalPower = 0
    AverageCOP = 0

    for i in range(1, total_zone_number+1):

        # requiredVariables
        electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom%C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20Strom%C2%ADkosten.
        t_supply_nom = t_supply
        t_return_nom = t_return
        FilteredData = Functions.get_filtered_data(i, name)
        tRoomSet = Functions.t_room_set(i, name)
        tOutside = FilteredData["TOutside"]
        heatingDemand = FilteredData["HeatingDemand"]
        tRoom = FilteredData["TRoom"]
        qualityGrade = 0.5

        # calculate tSupply and tReturn with linear solution
        # source --> https://www.viessmann.de/de/wohngebaeude/ratgeber/heizkurve-einstellen.html
        tSupply = Functions.t_supply_lin(t_supply_nom, i, name)
        tReturn = Functions.t_return_lin(t_return_nom, i, name)

        # get all parameters
        COP = (1/(1-tOutside/tSupply))*qualityGrade
        P_el = heatingDemand/COP
        costs = (electricityPrice/1000)*P_el  # divided by 1000, if electricity price is for kWh

        # put it in one dataframe
        data = pd.concat([COP, P_el, costs, tSupply, tReturn], axis=1, join='inner')
        data.columns = ["COP", "P_el", "costs", "tSupply", "tReturn"]

        # filter data not making sense (tSupply < tRoom)

        # sum up the costs
        zoneCosts = data['costs'].sum()
        TotalCosts += zoneCosts

        # sum up the power
        zonePower = data['P_el'].sum()
        TotalPower += zonePower

        # AverageCOP
        zoneCOP = data['COP'].sum()
        zoneAverageCOP = zoneCOP/len(data)
        AverageCOP += (zoneAverageCOP/total_zone_number)

    return TotalPower


def calculate_all_costs_real(total_zone_number, name, t_supply, t_return):

    TotalCosts = 0
    TotalPower = 0
    AverageCOP = 0

    for i in range(1, total_zone_number+1):

        # requiredVariables
        electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom%C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20Strom%C2%ADkosten.
        FilteredData = Functions.get_filtered_data(i, name)
        tRoomSet = Functions.t_room_set(i, name)
        tOutside = FilteredData["TOutside"]
        heatingDemand = FilteredData["HeatingDemand"]
        tRoom = FilteredData["TRoom"]
        qualityGrade = 0.5

        # calculate tSupply and tReturn with linear solution
        # source --> https://www.viessmann.de/de/wohngebaeude/ratgeber/heizkurve-einstellen.html
        tSupply = Functions.t_supply_paper(i, name, t_supply, t_return)
        tReturn = Functions.t_return_paper(i, name,  t_supply, t_return)

        # get all parameters
        COP = (1/(1-tOutside/tSupply))*qualityGrade
        P_el = heatingDemand/COP
        costs = (electricityPrice/1000)*P_el  # divided by 1000, if electricity price is for kWh

        # put it in one dataframe
        data = pd.concat([COP, P_el, costs, tSupply, tReturn], axis=1, join='inner')
        data.columns = ["COP", "P_el", "costs", "tSupply", "tReturn"]

        """
        # calculate supply temperature, source --> Supply Temperature Control Concepts, page 53
        c1 = (tSupplyNom-tReturnNom)/(tRoomNom-tOutsideNom)
        c2 = (c1*((tRoomNom-tOutsideNom)**(-1/n)))/delta_T_log_nom
        delta_T_out = tRoomNom - Functions.t_outside()
        c3 = math.e**(c2*(delta_T_out**(1-(1/n))))
        tSupplyOper = (tRoomNom-c3*(tRoomNom+c1*delta_T_out))/(1-c3)
        """

        # filter data not making sense (tSupply < tRoom)

        # sum up the costs
        zoneCosts = data['costs'].sum()
        TotalCosts += zoneCosts

        # sum up the power
        zonePower = data['P_el'].sum()
        TotalPower += zonePower

        # AverageCOP
        zoneCOP = data['COP'].sum()
        zoneAverageCOP = zoneCOP / len(data)
        AverageCOP += (zoneAverageCOP / total_zone_number)

    return (TotalCosts, TotalPower, AverageCOP)


def calculate_cop_real(total_zone_number, name, t_supply, t_return):

    TotalCosts = 0
    TotalPower = 0
    AverageCOP = 0

    for i in range(1, total_zone_number+1):

        # requiredVariables
        electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom%C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20Strom%C2%ADkosten
        FilteredData = Functions.get_filtered_data(i, name)
        tRoomSet = Functions.t_room_set(i, name)
        tOutside = FilteredData["TOutside"]
        heatingDemand = FilteredData["HeatingDemand"]
        tRoom = FilteredData["TRoom"]
        qualityGrade = 0.5

        # calculate tSupply and tReturn with linear solution
        # source --> https://www.viessmann.de/de/wohngebaeude/ratgeber/heizkurve-einstellen.html
        tSupply = Functions.t_supply_paper(i, name, t_supply, t_return)
        tReturn = Functions.t_return_paper(i, name,  t_supply, t_return)

        # get all parameters
        COP = (1/(1-tOutside/tSupply))*qualityGrade
        P_el = heatingDemand/COP
        costs = (electricityPrice/1000)*P_el  # divided by 1000, if electricity price is for kWh

        # put it in one dataframe
        data = pd.concat([COP, P_el, costs, tSupply, tReturn], axis=1, join='inner')
        data.columns = ["COP", "P_el", "costs", "tSupply", "tReturn"]

        """
        # calculate supply temperature, source --> Supply Temperature Control Concepts, page 53
        c1 = (tSupplyNom-tReturnNom)/(tRoomNom-tOutsideNom)
        c2 = (c1*((tRoomNom-tOutsideNom)**(-1/n)))/delta_T_log_nom
        delta_T_out = tRoomNom - Functions.t_outside()
        c3 = math.e**(c2*(delta_T_out**(1-(1/n))))
        tSupplyOper = (tRoomNom-c3*(tRoomNom+c1*delta_T_out))/(1-c3)
        """

        # filter data not making sense (tSupply < tRoom)

        # sum up the costs
        zoneCosts = data['costs'].sum()
        TotalCosts += zoneCosts

        # sum up the power
        zonePower = data['P_el'].sum()
        TotalPower += zonePower

        # AverageCOP
        zoneCOP = data['COP'].sum()
        zoneAverageCOP = zoneCOP / len(data)
        AverageCOP += (zoneAverageCOP / total_zone_number)

        return AverageCOP


def calculate_total_power_real(total_zone_number, name, t_supply, t_return):

    TotalCosts = 0
    TotalPower = 0
    AverageCOP = 0

    for i in range(1, total_zone_number+1):

        # requiredVariables
        electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom%C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20Strom%C2%ADkosten.
        FilteredData = Functions.get_filtered_data(i, name)
        tRoomSet = Functions.t_room_set(i, name)
        tOutside = FilteredData["TOutside"]
        heatingDemand = FilteredData["HeatingDemand"]
        tRoom = FilteredData["TRoom"]
        qualityGrade = 0.5

        # calculate tSupply and tReturn with linear solution
        # source --> https://www.viessmann.de/de/wohngebaeude/ratgeber/heizkurve-einstellen.html
        tSupply = Functions.t_supply_paper(i, name, t_supply, t_return)
        tReturn = Functions.t_return_paper(i, name, t_supply, t_return)

        # get all parameters
        COP = (1/(1-tOutside/tSupply))*qualityGrade
        P_el = heatingDemand/COP
        costs = (electricityPrice/1000)*P_el  # divided by 1000, if electricity price is for kWh

        # put it in one dataframe
        data = pd.concat([COP, P_el, costs, tSupply, tReturn], axis=1, join='inner')
        data.columns = ["COP", "P_el", "costs", "tSupply", "tReturn"]

        """
        # calculate supply temperature, source --> Supply Temperature Control Concepts, page 53
        c1 = (tSupplyNom-tReturnNom)/(tRoomNom-tOutsideNom)
        c2 = (c1*((tRoomNom-tOutsideNom)**(-1/n)))/delta_T_log_nom
        delta_T_out = tRoomNom - Functions.t_outside()
        c3 = math.e**(c2*(delta_T_out**(1-(1/n))))
        tSupplyOper = (tRoomNom-c3*(tRoomNom+c1*delta_T_out))/(1-c3)
        """

        # filter data not making sense (tSupply < tRoom)

        # sum up the costs
        zoneCosts = data['costs'].sum()
        TotalCosts += zoneCosts

        # sum up the power
        zonePower = data['P_el'].sum()
        TotalPower += zonePower

        # AverageCOP
        zoneCOP = data['COP'].sum()
        zoneAverageCOP = zoneCOP / len(data)
        AverageCOP += (zoneAverageCOP / total_zone_number)

        return TotalPower


# calculate

counter = 1
temp = {1: [90, 70], 2: [80, 60], 3: [75, 60], 4: [70, 55], 5: [65, 50], 6: [60, 50], 7: [55, 45], 8: [50, 40],
        9: [45, 35], 10: [40, 30]}
# source --> Performance of heat pumps retrofitted to radiator systems in existing
# buildings and measures to reduce space heating temperatures, page 9
for i in temp.values():
    costs_lin = []
    COP_lin = []
    Power_lin = []
    costs_real = []
    COP_real = []
    Power_real = []
    counter1 = 0

    for name in CreateBuilding.names:
        TotalZoneNumber = Functions.total_zone(name)

        # calculate linear
        linear_results = calculate_all_costs_lin(TotalZoneNumber, name, i[0], i[1])
        costs_lin.append(linear_results[0])
        Power_lin.append(linear_results[1])
        COP_lin.append(linear_results[2])

        # calculate real
        real_results = calculate_all_costs_real(TotalZoneNumber, name, i[0], i[1])
        costs_real.append(real_results[0])
        Power_real.append(real_results[1])
        COP_real.append(real_results[2])
        counter1 += 1
        print("Step " + str(counter) + "." + str(counter1) + " of " + str(len(temp)) + "." + str(len(CreateBuilding.names)) + " done!")

    print("Step " + str(counter) + " of " + str(len(temp)) + " done!")

    counter += 1


    #Create Dataframe
    col1 = 'names'
    col2 = 'costs_lin'
    col3 = 'COP_lin'
    col4 = 'Power_lin'
    col5 = 'costs_real'
    col6 = 'COP_real'
    col7 = 'Power_real'

    data_result = pd.DataFrame({col1: CreateBuilding.names, col2: costs_lin, col3: COP_lin, col4: Power_lin,
                                col5: costs_real, col6: COP_real, col7: Power_real})
    data_result.to_excel('data_result_tv' + str(i[0]) + 'and_tr' + str(i[1]) + '.xlsx', sheet_name='sheet1',
                         index=False)

print("Excel file is created. Find: D:\hkr-fme\Projects\Bachelorarbeit1")
"""
print(costs_lin)
print(COP_lin)
print(Power_lin)

print(costs_real)
print(COP_real)
print(Power_real)
"""

