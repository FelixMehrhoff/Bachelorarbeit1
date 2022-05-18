
# import all relevant packages
import os.path
from dymola.dymola_interface import DymolaInterface

# start Dymola
dymola = DymolaInterface()

# determine paths of the relevant packages
dir_aixlib = "D:/hkr-fme/Projects/AixLib/AixLib"
dir_model = "C:/Users/hkr-fme/TEASEROutput/BA"
dir_weaData = "C:/Users/hkr-fme/TEASEROutput/BA"
dir_result = 'D:/hkr-fme/Projects/Bachelorarbeit1/Results'

# open models
dymola.openModel(path=os.path.join(dir_aixlib, 'package.mo'))
dymola.openModel(path=os.path.join(dir_model, 'package.mo'))
dymola.openModel(path=os.path.join(dir_weaData, 'DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR'))

# translate model, which should be simulated
dymola.translateModel('BA.InstitutVersuchshalle.InstitutVersuchshalle')

# simulate model
output = dymola.simulateExtendedModel(
        problem='BA.InstitutVersuchshalle.InstitutVersuchshalle',
        startTime=0,
        stopTime=3.1536e+07,
        outputInterval=3600,
        method="Dassl",
        tolerance=0.0001,
        resultFile=os.path.join(dir_result, 'results'),
        finalNames=['multizone.TRad[1]'],
        )

# close Dymola
dymola.close()

# if output[0] == True, the simulation was successful
print(output)
