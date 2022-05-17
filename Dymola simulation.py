import os.path
from dymola.dymola_interface import DymolaInterface

dymola = DymolaInterface()

dir_aixlib = "D:/hkr-fme/Projects/AixLib/AixLib"

dir_model = "C:/Users/hkr-fme/TEASEROutput/BA"

dir_weaData = "C:/Users/hkr-fme/TEASEROutput/BA"

dir_result = 'D:/hkr-fme/Projects/Bachelorarbeit1/Results'

dymola.openModel(path=os.path.join(dir_aixlib, 'package.mo'))
dymola.openModel(path=os.path.join(dir_model, 'package.mo'))
dymola.openModel(path=os.path.join(dir_weaData, 'DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR'))

dymola.translateModel('BA.InstitutVersuchshalle.InstitutVersuchshalle')
overview = []
for i in range(0, 2):
    output = dymola.simulateExtendedModel(
        problem='BA.InstitutVersuchshalle.InstitutVersuchshalle',
        startTime=86400*i,
        stopTime=86400*(i+1),
        outputInterval=3600,
        method="Dassl",
        tolerance=0.0001,
        resultFile=os.path.join(dir_result, 'results'),
        finalNames=['multizone.TRad[1]', 'multizone.TRad[2]'],
    )
    overview.append(output[1])

dymola.close()
print(overview)
print(output)

