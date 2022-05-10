
from teaser.project import Project

prj = Project(load_data=True)
prj.name = 'BA'

prj.add_non_residential(method='bmvbs',
                        usage='office',
                        name='Institut Versuchshalle',
                        year_of_construction=2009, #https://www.baukunst-nrw.de/objekte/E.ON-Energy-Research-Center-Versuchshalle--1970.htm
                        number_of_floors=1,
                        height_of_floors=10,
                        net_leased_area=1260)


