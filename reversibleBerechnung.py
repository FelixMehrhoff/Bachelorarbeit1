
#benötigte Variablen
Q_ganzesHaus = [2.557, 2.884] #kW
T_vorlauf = 70  #°C
T_ruecklauf = 36.5 #°C
cp = 4.18 #kJ/(kg*K)
Tm_12 = 10 #°C, vielleicht die Außentemperatur, Verdampfung nur im Nassdampfgebiet angenommen
s4 = 1.384 #kJ/kg*K
s3 = 1.7716 #kJ/kg*K
strompreis=0.4 #€/kWh
betriebstage=340
zaehler = 1

for i in Q_ganzesHaus:


    #Energiebilanz um Heizung;
    m_heizkreislauf = i/(cp*(T_vorlauf-T_ruecklauf)) # ist ideale Flüssigkeit i.O.?


    #kleines q berechnen
    q_waermebedarf = i/m_heizkreislauf


    #Entropiebilanz um Wärmeübertrager, isentrop
    Tm_34 = -q_waermebedarf/(s4-s3)

    #Tag angeben:

    print("Für Tag " + str(zaehler) + " gilt: ")
    # Zähler hochzählen
    zaehler = zaehler+1

    #COP berechnen und ausgeben
    COP = 1/(1 - (Tm_12+273.15) / Tm_34)
    print("Der COP der Wärmepumpe beträgt: " + str(COP) + ".")

    #Wärmepumpenleistung berechnen und ausgeben
    P_el = i/COP
    print("Die Wärmepumpenleistung beträgt: " + str(P_el) + " kW.")



    #Stromkosten berechnen und ausgeben
    kosten= round(P_el*strompreis*24*betriebstage,2)
    if betriebstage < 356:
        print("Die jährlichen Stromkosten entsprechen bei " + str(betriebstage) + " gleichen Betriebstagen: " + str(kosten) + "€.")
    else:
        print("Die jährlichen Stromkosten entsprechen bei Dauerbetrieb mit 365 gleichen Betriebstagen" + str(kosten) + "€.")

