import Functions
import numpy as np
import pandas as pd


def calculateAllCosts(total_zone_number):

    TotalCosts = 0

    for i in range(1, total_zone_number+1):

        # requiredVariables
        electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom%C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20Strom%C2%ADkosten.
        tRoomNom = 293.15  # K, source--> Recknagel, page 1375
        tSupplyNom = 348.15  # K, source--> Recknagel, page 1375
        tReturnNom = 338.15  # K, source--> Recknagel, page 1375
        delta_T_log_nom = (tSupplyNom-tReturnNom)/np.log((tSupplyNom-tRoomNom)/(tReturnNom-tRoomNom))  # source -->Supply Temperature Control Concepts, page 51
        tOutsideNom = Functions.t_outside_nom(68159)+273.15  # enter PLZ of weather data, source --> DIN_TS 12831-1
        n = 1.3  # for radiator, source Recknagel, page 1375
        tRoomSet = Functions.t_room_set(i)
        tOutside = Functions.t_outside()
        heatingDemand = Functions.heating_demand(i)
        tRoom = Functions.t_room(i)

        # calculate tSupply and tReturn with linear solution
        # source --> https://www.viessmann.de/de/wohngebaeude/ratgeber/heizkurve-einstellen.html
        tSupply = Functions.t_supply_lin(373.15, 274.15)
        tReturn = Functions.t_return_lin(353.15, 274.15)

        # get tLog of the heatpump
        # +2K, then heat transfer always possible
        tLogHeatpump = (tSupply-tReturn)/np.log((tSupply+2-tRoomSet)/(tReturn+2-tRoomSet))

        # get all parameters
        COP = 1/(1-tOutside/(tLogHeatpump+294.15))
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

        for y in data.index:
            if data['tSupply'][y] < 294.15:
                data['P_el'][y] = 0

        # sum up the costs
        zoneCosts = data['costs'].sum()
        TotalCosts += zoneCosts

    return TotalCosts


TotalZoneNumber = Functions.total_zone()
c = int(TotalZoneNumber.iloc[0]['raw'])


print(calculateAllCosts(c))


"""
create Excel-file
workbook = xlsxwriter.Workbook('results.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Tag')
worksheet.write('B1', 'COP')
worksheet.write('C1', 'electrical power [kW]')
worksheet.write('D1', 'price [€/kWh]')

row = 1
col = 0

for day, cop, power, price in result:
    worksheet.write(row, col, day)
    worksheet.write(row, col + 1, cop)
    worksheet.write(row, col + 2, power)
    worksheet.write(row, col + 3, price)
    row += 1

workbook.close()

"""
