# import all relevant packages
from ebcpy import TimeSeriesData
import matplotlib.pyplot as plt


def getDataList ():
    # create DataFrame
    ResultData = TimeSeriesData(r"D:\hkr-fme\Projects\Bachelorarbeit1\Results\results.mat")

    # filter DataFrame
    FilteredData = ResultData.loc[:, ["multizone.TRad[1]", "multizone.TRad[2]"]]

    # add Data to a list
    x = FilteredData.to_numpy()
    print(x)
    y = x.tolist()
    print(y)

    DataList = {}

    for i in range(0, len(x)):
        DataList[i] = y[i]

    return DataList

# tests
"""
for i in range(0, len(x)):
    if x[i][0] > 300:
        print(i)


print(T_Rad_dict)


plt.figure()
plt.plot(ResultData.loc[:, ("multizone.TRad[1]", "raw")], label="T_Rad 1", color="blue")
plt.plot(ResultData.loc[:, ("multizone.TRad[2]", "raw")], label="T_Rad 2", color="red")
plt.legend()
plt.show()
"""
