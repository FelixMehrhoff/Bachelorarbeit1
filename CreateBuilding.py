
from ebcpy import TimeSeriesData

from teaser.logic.buildingobjects.thermalzone import ThermalZone
from teaser.project import Project
import teaser.logic.utilities as utilities
import teaser.logic.buildingobjects.buildingphysics.window as window
import os



prj = Project(load_data=True)
prj.name = 'BA'
prj.number_of_elements_calc = 2
prj.merge_windows_calc = False
prj.used_library_calc = 'AixLib'
prj._weather_file_path = 'D:\hkr-fme\Projects\TEASER\teaser\data\input\inputdata\weatherdata'

prj.add_non_residential(method='bmvbs',
                        usage='office',
                        name='InstitutVersuchshalle',
                        year_of_construction=2015, #https://www.baukunst-nrw.de/objekte/E.ON-Energy-Research-Center-Versuchshalle--1970.htm
                        number_of_floors=1,
                        height_of_floors=10.0,
                        net_leased_area=1260.0)
prj.add_residential(
        method='iwu',
        usage='single_family_dwelling',
        name="Home",
        year_of_construction=1947,
        number_of_floors=4,
        height_of_floors=2.5,
        net_leased_area=200.0)

prj.retrofit_all_buildings(
        year_of_retrofit=2002,
        type_of_retrofit="adv_retrofit",
        window_type='Alu- oder Stahlfenster, Isolierverglasung',
        material='EPS_perimeter_insulation_top_layer')

prj.dir_reference_results = utilities.get_full_path(
        os.path.join(
            "examples",
            "examplefiles",
            "ReferenceResults",
            "Dymola"))

print(prj.dir_reference_results)

prj.weather_file_path = utilities.get_full_path(
        os.path.join(
            "data",
            "input",
            "inputdata",
            "weatherdata",
            "DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"))

path = prj.export_aixlib(
        internal_id=None,
        path=None)


prj.calc_all_buildings()




