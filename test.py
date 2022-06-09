import Functions
from matplotlib import pyplot as plt

y = Functions.supply_my_formula()
x = Functions.t_supply_lin(373.15)

plt.plot(x-y)
# plt.plot(y)
plt.show()