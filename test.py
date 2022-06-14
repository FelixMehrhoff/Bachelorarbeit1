import Functions
import matplotlib.pyplot as plt

data = Functions.get_filtered_data(1)
x = data["TOutside"]
y = Functions.t_supply_paper(1)
z = Functions.t_return_paper(1)

plt.scatter(x-273.15, y-273.15)
plt.scatter(x-273.15, z-273.15)
plt.show()