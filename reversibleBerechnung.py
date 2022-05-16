
import xlsxwriter

# requiredVariables
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

for i in Q_wholeHouse:
    # energy balance around the heating;
    m_heatingCircuit = i / (cp_water * (T_flow - T_return))  # ideal liquid

    # calculate specific q
    q_heatDemand = i / m_heatingCircuit

    # entropy balance around the isentropic heat exchanger
    Tm_34 = q_heatDemand / (s3 - s4)

    # specify day:
    print("For day " + str(counter) + " applies: ")

    # calculate and give out COP
    COP = 1 / (1 - (Tm_12 + 273.15) / Tm_34)
    print("The COP of the heat pump is: " + str(COP) + ".")

    # calculate and giv out power of heat pump
    P_el = i / COP
    print("The power of the heat pump is" + str(P_el) + " kW.")

    # calculate and give out costs for electricity
    cost = P_el * electricityPrice
    print("The costs per hour are" + str(round(cost, 2)) + " €/kWh")

    summary = [counter, round(COP, 2), round(P_el, 2), round(cost, 2)]
    result.append(summary)

    # count up
    counter = counter + 1

print(result)

# create Excel-file
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
