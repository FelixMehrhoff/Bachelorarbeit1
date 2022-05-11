
import pathlib
import numpy as np
import matplotlib.pyplot as plt
from ebcpy import TimeSeriesData
from teaser.project import Project
import teaser.logic.utilities as utilities
import os

prj = Project(load_data=True)
prj.name = 'BA'
prj.number_of_elements_calc = 2
prj.merge_windows_calc = True
prj.used_library_calc = 'AixLib'
prj._weather_file_path = 'D:\hkr-fme\Projects\TEASER\teaser\data\input\inputdata\weatherdata'

prj.add_non_residential(method='bmvbs',
                        usage='office',
                        name='Institut Versuchshalle',
                        year_of_construction=2009, #https://www.baukunst-nrw.de/objekte/E.ON-Energy-Research-Center-Versuchshalle--1970.htm
                        number_of_floors=1,
                        height_of_floors=10.0,
                        net_leased_area=1260.0)
prj.add_residential(
        method='iwu',
        usage='single_family_dwelling',
        name="Home",
        year_of_construction=2004,
        number_of_floors=4,
        height_of_floors=2.5,
        net_leased_area=200.0)

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


