import Functions
import matplotlib.pyplot as plt
import numpy as np
import CreateBuilding
import xlwt
from xlwt import Workbook
import pandas as pd

"""
Data = Functions.get_filtered_data(1, "StandardAtHome2007")
t = Functions.t_supply_paper(1, "StandardAtHome2007", 75, 65)
y = Functions.t_supply_lin(75, 1, "StandardAtHome2007")
# x = Functions.t_return_lin(65, 1, "Zuhause2007Uvalue04")
# r = Functions.t_return_paper(1, "Zuhause2007Uvalue04")
tOut = Data["TOutside"]

plt.scatter(tOut - 273.15, t - 273.15)
plt.scatter(tOut - 273.15, y - 273.15)
#plt.scatter(tOut - 273.15, x - 273.15)
#plt.scatter(tOut - 273.15, r - 273.15)
plt.show()
"""
"""
x = Functions.get_q_nom('StandardAtHome2007')
y = Functions.get_q_nom("WindowAtHome2007")
print(x)
print(y)




heat_capac = []
Rse = 0.04
Rsi = 0.13
thickness = 0.024
U_Values = [0.4, 0.6, 0.8, 1, 1.2, 2, 2.5, 3, 4, 5]

for x in U_Values:
    y = thickness/((1/x)-Rsi-Rse)
    heat_capac.append(y)

print(heat_capac)
"""
"""
Data = Functions.get_filtered_data(1, "WindowRowHouse1920")
tLim = Functions.get_t_lim(1, "WindowRowHouse1920")
tAirNom = Functions.get_t_air_nom(1, "WindowRowHouse1920")
TRoom = Data["TRoom"]
tOutside = Data["TOutside"]
TSupplyNom1 = 90+273.15
TReturnNom1 = 70+273.15
TSupplyNom2 = 70+273.15
TReturnNom2 = 55+273.15
n = 1.3

# calculations
Q_rel = (tLim-tOutside)/(tLim-tAirNom)
TSupply = TRoom + ((((TSupplyNom1+TReturnNom1)/2)-TRoom)*(Q_rel**(1/n))) + (((TSupplyNom1-TReturnNom1)/2)*Q_rel)
TSupply2 = TRoom + ((((TSupplyNom2+TReturnNom2)/2)-TRoom)*(Q_rel**(1/n))) + (((TSupplyNom2-TReturnNom2)/2)*Q_rel)

plt.scatter(tOutside - 273.15, TSupply - 273.15)
#plt.scatter(tOutside - 273.15, TSupply2 - 273.15)
plt.show()
"""

"""
kind = CreateBuilding.kind
years = CreateBuilding.all_years
zone_number = 1
names_standard = []
for i in years:
    names_standard.append("Standard" + kind + str(i))

df = pd.DataFrame(columns=names_standard)

print(df)
"""

