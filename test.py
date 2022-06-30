import Functions
import matplotlib.pyplot as plt
import numpy as np
import CreateBuilding

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
