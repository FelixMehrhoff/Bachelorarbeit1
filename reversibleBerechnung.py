import xlsxwriter

# requiredVariables
import DataList
import math
import numpy as np

Q_wholeHouse = [2.557, 2.884]  # kW
T_flow = 70  # °C
T_return = 60  # °C
cp_water = 4.18  # kJ/(kg*K)
Tm_12 = 10  # °C, maybe the outside temperature,  evaporation only in wet steam area
s4 = 1.384  # kJ/kg*K
s3 = 1.7716  # kJ/kg*K
electricityPrice = 0.4  # €/kWh
counter = 1
result = []

x = DataList.getDataList()
result = {}

for key in x:
    # from standard conditions to operational conditions
    Q_operational = x[key][0] * (
                ((x[key][1] - x[key][2]) / (np.log((x[key][1] - x[key][3]) / (x[key][2] - x[key][3])))) / 10 / (
            np.log(55 / 45)))

    # energy balance around the heating
    m_heatingCircuit = Q_operational / (cp_water * (x[key][1] - x[key][2]))  # ideal liquid

    # calculate specific q
    q_heatDemand = Q_operational / m_heatingCircuit

    # entropy balance around the isentropic heat exchanger
    Tm_34 = q_heatDemand / (s3 - s4)

    # calculate and add COP to result
    COP = 1 / (1 - (x[key][4]) / Tm_34)

    # calculate and giv out power of heat pump
    P_el = Q_operational / COP

    # calculate and give out costs for electricity
    cost = P_el * electricityPrice
    result = {key: [COP, P_el, cost]}

# create Excel-file
"""
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
