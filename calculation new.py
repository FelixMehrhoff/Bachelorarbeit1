import Functions
import numpy as np
import pandas as pd
import CreateBuilding


#  calculate unretrofitted building with old heating curve

kind = CreateBuilding.kind
years = CreateBuilding.all_years
zone_number = 1
names_standard = []
cp_m = 0
k_A = 0
quality_grade = 0.5  # schwankt in Realität --> Ausblick
electricityPrice = 0.3619  # €/kWh, source --> https://www.vergleich.de/strompreise.html#:~:text=Der%20aktuelle%20Strom
# %C2%ADpreis%20liegt%20laut%20Bundes%C2%ADverband%20der%20Energie-,kWh%20pro%20Jahr%20ca.%201.167%20%E2%82%AC%20an%20
# Strom%C2%ADkosten.


for i in years:
    names_standard.append("Standard" + kind + str(i))

print(names_standard)

temp = {1: [90, 70], 2: [80, 60], 3: [75, 60], 4: [70, 55], 5: [65, 50], 6: [60, 50], 7: [55, 45], 8: [50, 40],
        9: [45, 35], 10: [40, 30]}
test = {1: [90, 70], 2: [80, 60] }
all_costs = []
all_P_el = []
all_COP = []
all_COP_opt = []
all_P_el_opt = []
all_costs_opt = []
area = []
types = []
counter = 1
n = 1.3  # Heizkörperexponent

"""
for j in names_standard:
    total_zone_number = Functions.total_zone(j)
    total_heating_demand = 0


    for l in range (1, total_zone_number+1):
        data1 = Functions.get_filtered_data(l, j)
        heatingDemand = data1["HeatingDemand"]
        total_heating_demand += heatingDemand

    data = Functions.get_filtered_data(zone_number, j)
    q_nom = Functions.get_q_nom(j)

    t_outside = data["TOutside"]

    for k in test.values():
        bul_COP = []
        bul_costs = []
        bul_P_el = []
        counter = 1
        heating_curve_old = Functions.t_supply_paper(zone_number, j, k[0], k[1])
        t_return_old = Functions.t_return_paper(zone_number, j, k[0], k[1])

        COP = (1/(1-t_outside/heating_curve_old))*quality_grade

        P_el = total_heating_demand/COP

        costs = (electricityPrice / 1000) * P_el  # divided by 1000, if electricity price is for kWh

        data1 = pd.concat([COP, P_el, costs], axis=1, join='inner')
        data1.columns = ["COP", "P_el", "costs"]

        Total_COP_sum = data1['COP'].sum()
        Total_COP = Total_COP_sum / len(data)

        Total_P_el = data1['P_el'].sum()

        Total_costs = data1['costs'].sum()

        all_COP.append(float(Total_COP))
        all_costs.append(float(Total_costs))
        all_P_el.append(float(Total_P_el))


        types.append(j + "_" + str(k[0]) + "/" + str(k[1]))


# create Dataframe
col1 = 'types'
col2 = 'COP'
col3 = 'costs'
col4 = 'P_el'

data_result = pd.DataFrame({col1: types, col2: all_COP, col3: all_costs, col4: all_P_el})
data_result.to_excel('Standard_' + kind + '.xlsx', sheet_name='sheet1',
                         index=False)


#  calculate retrofitted building with old heating curve
"""

for year in years:
    for y in ('Standard', 'Window', 'WindowAdv', 'Rooftop', 'Groundfloor', 'Outerwall'):
        x = y + kind + str(year)
        j = 'Standard' + kind + str(year)
        total_zone_number = Functions.total_zone(x)
        total_heating_demand = 0

        for l in range(1, total_zone_number + 1):
            data1 = Functions.get_filtered_data(l, x)
            heatingDemand = data1["HeatingDemand"]
            total_heating_demand += heatingDemand

        data = Functions.get_filtered_data(zone_number, x)

        t_outside = data["TOutside"]
        heating_curve_old = None

        for k in test.values():

            # old heating curve
            heating_curve_old = Functions.t_supply_paper(zone_number, j, k[0], k[1])

            #  calculation for old heating curve
            COP = (1 / (1 - t_outside / heating_curve_old)) * quality_grade

            P_el = total_heating_demand / COP

            costs = (electricityPrice / 1000) * P_el  # divided by 1000, if electricity price is for kWh

            data1 = pd.concat([COP, P_el, costs], axis=1, join='inner')
            data1.columns = ["COP", "P_el", "costs"]

            Total_COP_sum = data1['COP'].sum()
            Total_COP = Total_COP_sum / len(data)

            Total_P_el = data1['P_el'].sum()

            Total_costs = data1['costs'].sum()

            all_COP.append(float(Total_COP))
            all_costs.append(float(Total_costs))
            all_P_el.append(float(Total_P_el))
            area.append(float(Functions.get_area(x)))
            types.append(x + "_" + str(k[0]) + "/" + str(k[1]))

            # get values for optimal heating curve
            q_nom_old = Functions.get_q_nom(j)
            m_cp = q_nom_old / (k[0] - k[1])
            t_room = Functions.t_room_set(zone_number, j)
            t_log = (k[0] - k[1]) / (np.log(((k[0]+273.15) - t_room) / ((k[1]+273.15) - t_room)))

            kA = q_nom_old / (t_log ** n)

            # calculation with optimal heating curve
            # get new heating curve
            q_nom_new = Functions.get_q_nom(x)
            spread_heating = q_nom_new/m_cp
            t_supply_opt = Functions.optimal_t_supply(q_nom_new, spread_heating, n, kA, t_room)-273.15
            t_return_opt = t_supply_opt-spread_heating-273.15
            heating_curve_new = Functions.t_supply_paper(zone_number, x, t_supply_opt, t_return_opt)

            # caluclate
            COP_opt = (1 / (1 - t_outside / heating_curve_new)) * quality_grade
            print(COP_opt)

            P_el_opt = total_heating_demand / COP_opt

            costs_opt = (electricityPrice / 1000) * P_el_opt  # divided by 1000, if electricity price is for kWh

            data2 = pd.concat([COP_opt, P_el_opt, costs_opt], axis=1, join='inner')
            data2.columns = ["COP_opt", "P_el_opt", "costs_opt"]

            Total_COP_sum_opt = data2['COP_opt'].sum()
            Total_COP_opt = Total_COP_sum_opt / len(data)

            Total_P_el_opt = data2['P_el_opt'].sum()

            Total_costs_opt = data2['costs_opt'].sum()

            all_COP_opt.append(float(Total_COP_opt))
            all_costs_opt.append(float(Total_costs_opt))
            all_P_el_opt.append(float(Total_P_el_opt))



print(types)

# create Dataframes and excels
col1 = 'types'
col2 = 'COP'
col3 = 'costs'
col4 = 'P_el'
col5 = 'area'
col6 = 'COP_opt'
col7 = 'costs_opt'
col8 = 'P_el_opt'

data_result_standard = pd.DataFrame({col1: types, col2: all_COP, col3: all_costs, col4: all_P_el, col5: area})
data_result_standard.to_excel('Vergleich_mit_gleicher_Heizkurve_' + kind + '.xlsx', sheet_name='sheet1', index=False)

data_result_optimal = pd.DataFrame({col1: types, col6: all_COP_opt, col7: all_costs_opt, col8: all_P_el_opt, col5: area})
data_result_optimal.to_excel('Vergleich_mit_optimaler_Heizkurve_' + kind + '.xlsx', sheet_name='sheet1', index=False)








