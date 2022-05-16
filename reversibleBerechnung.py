
import xlsxwriter


#benötigte Variablen
Q_ganzesHaus = [2.557, 2.884] #kW
T_vorlauf = 70  #°C
T_ruecklauf = 36.5 #°C
cp_wasser = 4.18 #kJ/(kg*K)
Tm_12 = 10 #°C, vielleicht die Außentemperatur, Verdampfung nur im Nassdampfgebiet angenommen
s4 = 1.384 #kJ/kg*K
s3 = 1.7716 #kJ/kg*K
strompreis=0.4 #€/kWh
betriebstage=340
zaehler = 1
ergebnis = []


for i in Q_ganzesHaus:


    #Energiebilanz um Heizung;
    m_heizkreislauf = i/(cp_wasser*(T_vorlauf-T_ruecklauf)) # ist ideale Flüssigkeit i.O.?


    #kleines q berechnen
    q_waermebedarf = i/m_heizkreislauf


    #Entropiebilanz um Wärmeübertrager, isentrop
    Tm_34 = q_waermebedarf/(s3-s4)

    #Tag angeben:

    print("Für Tag " + str(zaehler) + " gilt: ")


    #COP berechnen und ausgeben
    COP = 1/(1 - (Tm_12+273.15) / Tm_34)
    print("Der COP der Wärmepumpe beträgt: " + str(COP) + ".")

    #Wärmepumpenleistung berechnen und ausgeben
    P_el = i/COP
    print("Die Wärmepumpenleistung beträgt: " + str(P_el) + " kW.")



    #Stromkosten berechnen und ausgeben
    kosten = P_el*strompreis
    print("Die Kosten pro Stunde betragen: " + str(round(kosten, 2)) + " €/kWh")

    list =[zaehler, round(COP, 2), round(P_el, 2), round(kosten, 2)]
    ergebnis.append(list)


    # Zähler hochzählen
    zaehler = zaehler + 1

print(ergebnis)

#Excel-Datei inizieren
workbook = xlsxwriter.Workbook('Auswertung.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'Tag')
worksheet.write('B1', 'COP')
worksheet.write('C1', 'elektrische Leistung [kW]')
worksheet.write('D1', 'Preis [€/kWh]')

row=1
col=0


for day, cop, power, price in ergebnis:
    worksheet.write(row, col, day)
    worksheet.write(row, col+1, cop)
    worksheet.write(row, col+2, power)
    worksheet.write(row, col+3, price)
    row += 1

workbook.close()

