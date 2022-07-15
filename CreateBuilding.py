
from ebcpy import TimeSeriesData

from teaser.logic.buildingobjects.thermalzone import ThermalZone
from teaser.project import Project
import teaser.logic.utilities as utilities
import teaser.logic.buildingobjects.buildingphysics.window as window
import os
import json


"""
prj = Project(load_data=True)
prj.name = 'BA'
prj.number_of_elements_calc = 4
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
        year_of_construction=1918,
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

"""

# start teaser
from teaser.project import Project

names = []
prj = Project(load_data=True)
prj.name = "BA1"


# define methods
def create_single_family_house_long_method(year, u_value):

    Rse = 0.04
    Rsi = 0.13
    thickness = 0.024
    thermal_conduction = thickness / ((1 / u_value) - Rsi - Rse)

    # create building
    from teaser.logic.buildingobjects.building import Building

    bldg = Building(parent=prj)
    bldg.name = "Zuhause " + str(year) + ", Uvalue: " + str(u_value)
    names.append(bldg.name)
    bldg.street_name = "AwesomeAvenue42"
    bldg.city = "46325FantasticTown"
    bldg.year_of_construction = year
    bldg.number_of_floors = 1
    bldg.height_of_floors = 3.5

    # Instantiate a ThermalZone class

    from teaser.logic.buildingobjects.thermalzone import ThermalZone

    tz = ThermalZone(parent=bldg)
    tz.name = "LivingRoom"
    tz.area = 140.0
    tz.volume = tz.area * bldg.number_of_floors * bldg.height_of_floors
    tz.infiltration_rate = 0.5

    # Instantiate BoundaryConditions and load conditions for `Living`.

    from teaser.logic.buildingobjects.useconditions \
        import UseConditions

    tz.use_conditions = UseConditions(parent=tz)
    tz.use_conditions.load_use_conditions("Living", prj.data)

    # Define two building elements reflecting a pitched roof (south = 180° and
    # north = 0°).

    from teaser.logic.buildingobjects.buildingphysics.rooftop import Rooftop

    roof_south = Rooftop(parent=tz)
    roof_south.name = "Roof_South"
    roof_south.area = 75.0
    roof_south.orientation = 180.0
    roof_south.tilt = 55.0
    roof_south.inner_convection = 1.7
    roof_south.outer_convection = 20.0
    roof_south.inner_radiation = 5.0
    roof_south.outer_radiation = 5.0

    roof_north = Rooftop(parent=tz)
    roof_north.name = "Roof_North"
    roof_north.area = 75.0
    roof_north.orientation = 0.0
    roof_north.tilt = 55.0
    roof_north.inner_convection = 1.7
    roof_north.outer_convection = 20.0
    roof_north.inner_radiation = 5.0
    roof_north.outer_radiation = 5.0

    # define the wall constructions

    from teaser.logic.buildingobjects.buildingphysics.layer import Layer

    # First layer south

    layer_s1 = Layer(parent=roof_south, id=0)
    layer_s1.thickness = 0.3

    from teaser.logic.buildingobjects.buildingphysics.material import Material

    material_s1 = Material(layer_s1)
    material_s1.name = "Insulation"
    material_s1.density = 120.0
    material_s1.heat_capac = 0.04
    material_s1.thermal_conduc = 1.0

    # Second layer south

    layer_s2 = Layer(parent=roof_south, id=1)
    layer_s2.thickness = 0.15

    material_s2 = Material(layer_s2)
    material_s2.name = "Tile"
    material_s2.density = 1400.0
    material_s2.heat_capac = 0.6
    material_s2.thermal_conduc = 2.5

    # First layer north

    layer_n1 = Layer(parent=roof_north, id=0)
    layer_n1.thickness = 0.3

    from teaser.logic.buildingobjects.buildingphysics.material import Material

    material_n1 = Material(layer_n1)
    material_n1.name = "Insulation"
    material_n1.density = 120.0
    material_n1.heat_capac = 0.04
    material_n1.thermal_conduc = 1.0

    # Second layer north

    layer_n2 = Layer(parent=roof_north, id=1)
    layer_n2.thickness = 0.15

    material_n2 = Material(layer_n2)
    material_n2.name = "Tile"
    material_n2.density = 1400.0
    material_n2.heat_capac = 0.6
    material_n2.thermal_conduc = 2.5

    # Another option is to use the database for typical wall constructions,
    # but set area, tilt, orientation individually. To simplify code,
    # we save individual information for exterior walls, interior walls into
    # dictionaries.
    # outer walls
    # {'name_of_wall': [area, tilt, orientation]}
    # interior walls
    # {'name_of_wall': [area, tilt, orientation]}

    from teaser.logic.buildingobjects.buildingphysics.outerwall import OuterWall

    out_wall_dict = {"OuterWall_north": [10.0, 90.0, 0.0],
                     "OuterWall_east": [14.0, 90.0, 90.0],
                     "OuterWall_south": [10.0, 90.0, 180.0],
                     "OuterWall_west": [14.0, 90.0, 270.0]}

    # For ground floors the orientation is always -2

    ground_floor_dict = {"GroundFloor": [100.0, 0.0, -2]}

    from teaser.logic.buildingobjects.buildingphysics.innerwall import InnerWall

    in_wall_dict = {"InnerWall1": [10.0],
                    "InnerWall2": [14.0],
                    "InnerWall3": [10.0]}

    for key, value in out_wall_dict.items():
        # Instantiate class, key is the name
        out_wall = OuterWall(parent=tz)
        out_wall.name = key
        # Use load_type_element() function of the building element, and pass
        # over the year of construction of the building and the type of
        # construction (in this case `heavy`).

        out_wall.load_type_element(
            year=bldg.year_of_construction,
            construction='heavy')

        # area, tilt and orientation need to be set individually.

        out_wall.area = value[0]
        out_wall.tilt = value[1]
        out_wall.orientation = value[2]

    # Repeat the procedure for inner walls and ground floors

    for key, value in in_wall_dict.items():
        in_wall = InnerWall(parent=tz)
        in_wall.name = key
        in_wall.load_type_element(
            year=bldg.year_of_construction,
            construction='heavy')
        in_wall.area = value[0]

    from teaser.logic.buildingobjects.buildingphysics.groundfloor import \
        GroundFloor

    for key, value in ground_floor_dict.items():
        ground = GroundFloor(parent=tz)
        ground.name = key
        ground.load_type_element(
            year=bldg.year_of_construction,
            construction='heavy')
        ground.area = value[0]
        ground.tilt = value[1]
        ground.orientation = value[2]

    from teaser.logic.buildingobjects.buildingphysics.window import Window

    win_dict = {"Window_east": [5.0, 90.0, 90.0],
                "Window_south": [8.0, 90.0, 180.0],
                "Window_west": [5.0, 90.0, 270.0]}

    for key, value in win_dict.items():
        win = Window(parent=tz)
        win.name = key
        win.area = value[0]
        win.tilt = value[1]
        win.orientation = value[2]

        # Additional to the already known attributes the window has
        # additional attributes. Window.g_value describes the solar gain
        # through windows, a_conv the convective heat transmission due to
        # absorption of the window on the inner side. shading_g_total and
        # shading_max_irr refers to the shading (solar gain reduction of the
        # shading and shading_max_irr the threshold of irradiance to
        # automatically apply shading).

        win.inner_convection = 1.7
        win.inner_radiation = 5.0
        win.outer_convection = 20.0
        win.outer_radiation = 5.0
        win.g_value = 0.789
        win.a_conv = 0.03
        win.shading_g_total = 0.0
        win.shading_max_irr = 180.0

        # One equivalent layer for windows

        win_layer = Layer(parent=win)
        win_layer.id = 1
        win_layer.thickness = 0.024

        # Material for glass

        win_material = Material(win_layer)
        win_material.name = "GlasWindow"
        win_material.thermal_conduc = thermal_conduction
        win_material.transmittance = 0.9


def create_single_family_house_tabula_standard(year, name, floors, floor_height, area, neighbours):
    prj.add_residential(
        method='tabula_de',
        usage='single_family_house',
        name=name + str(year),
        year_of_construction=year,
        number_of_floors=floors,
        height_of_floors=floor_height,
        net_leased_area=area,
        construction_type='tabula_standard',
        neighbour_buildings=neighbours)
    names.append(name + str(year))


def create_single_family_house_tabula_window(year, name,  floors, floor_height, area, neighbours):
    prj.add_residential(
        method='tabula_de',
        usage='single_family_house',
        name=name + str(year),
        year_of_construction=year,
        number_of_floors=floors,
        height_of_floors=floor_height,
        net_leased_area=area,
        construction_type='tabula_window',
        neighbour_buildings=neighbours)
    names.append(name + str(year))


def create_single_family_house_tabula_window_adv(year, name,  floors, floor_height, area, neighbours):
    prj.add_residential(
        method='tabula_de',
        usage='single_family_house',
        name=name + str(year),
        year_of_construction=year,
        number_of_floors=floors,
        height_of_floors=floor_height,
        net_leased_area=area,
        construction_type='tabula_adv_window',
        neighbour_buildings=neighbours)
    names.append(name + str(year))


def create_single_family_house_tabula_rooftop(year, name,  floors, floor_height, area, neighbours):
    prj.add_residential(
        method='tabula_de',
        usage='single_family_house',
        name=name + str(year),
        year_of_construction=year,
        number_of_floors=floors,
        height_of_floors=floor_height,
        net_leased_area=area,
        construction_type='tabula_rooftop',
        neighbour_buildings=neighbours)
    names.append(name + str(year))


def create_single_family_house_tabula_groundfloor(year, name,  floors, floor_height, area, neighbours):
    prj.add_residential(
        method='tabula_de',
        usage='single_family_house',
        name=name + str(year),
        year_of_construction=year,
        number_of_floors=floors,
        height_of_floors=floor_height,
        net_leased_area=area,
        construction_type='tabula_groundfloor',
        neighbour_buildings=neighbours)
    names.append(name + str(year))


def create_single_family_house_tabula_outerwall(year, name,  floors, floor_height, area, neighbours):
    prj.add_residential(
        method='tabula_de',
        usage='single_family_house',
        name=name + str(year),
        year_of_construction=year,
        number_of_floors=floors,
        height_of_floors=floor_height,  # https://www.fertighaus.de/ratgeber/hausbau/deckenhoehe-bei-neubauten/
        net_leased_area=area,
        construction_type='tabula_outerwall',
        neighbour_buildings=neighbours)
    names.append(name + str(year))



# create houses



kind = "RowHouse"
floors = 4
floor_height = 2.4  # https://www.fertighaus.de/ratgeber/hausbau/deckenhoehe-bei-neubauten/
area = 75  # m^2
neighbours = 4
all_years = (1880, 1925, 1954, 1960)  # all_years = (1840, 1880, 1925, 1954,
# 1960, 1974, 1982, 1990, 1999, 2006, 2014)

"""
# define data in following order [year, floors, floor_height, area, neighbours]
data_SFH = {1:  [1840, 2, 2.94, 218.9, 0],
            2:  [1880, 2, 2.94, 141.8, 0],
            3:  [1925, 2, 2.94, 302.5, 0],
            4:  [1954, 1, 2.94, 111.1, 0],
            5:  [1960, 1, 2.94, 121.2, 0],
            6:  [1974, 1, 2.94, 173.3, 0],
            7:  [1982, 2, 2.94, 215.6, 1],
            8:  [1990, 1, 2.94, 150.2, 1],
            9:  [1999, 1, 2.94, 121.9, 0],
            10: [2006, 2, 2.94, 146.5, 0],
            11: [2014, 2, 2.94, 176.4, 0]}
data_RH = {1:  [1880, 2, 2.85, 96.00, 2],
           2:  [1925, 2, 2.85, 112.8, 2],
           3:  [1954, 2, 2.85, 149.6, 1],
           4:  [1960, 2, 2.85, 117.4, 2],
           5:  [1974, 2, 2.85, 106.3, 2],
           6:  [1982, 2, 2.85, 108.3, 2],
           7:  [1990, 2, 2.85, 127.6, 1],
           8:  [1999, 2, 2.85, 148.8, 2],
           9:  [2006, 2, 2.85, 151.9, 1],
           10: [2014, 2, 2.85, 184.3, 1]}
data_MFH = {1:  [1840, 4, 3.21, 677.50, 0],
            2:  [1880, 4, 3.21, 312.40, 2],
            3:  [1925, 3, 3.21, 385.00, 0],
            4:  [1954, 3, 3.21, 632.30, 0],
            5:  [1960, 4, 3.21, 3129.1, 1],
            6:  [1974, 4, 3.21, 468.60, 0],
            7:  [1982, 3, 3.21, 654.00, 0],
            8:  [1990, 3, 3.21, 778.10, 0],
            9:  [1999, 4, 3.21, 834.90, 1],
            10: [2006, 3, 3.21, 2190.1, 1],
            11: [2014, 5, 3.21, 1287.0, 0]}
data_GMH = {1: [1880, 5, 3.21, 829.40, 2],
            2: [1925, 5, 3.21, 1484.0, 1],
            3: [1954, 5, 3.21, 1602.7, 0],
            4: [1960, 8, 3.21, 3887.4, 0],
            5: [1974, 8, 3.21, 3322.0, 0]}


for i in data_SFH.values():
    create_single_family_house_tabula_standard(i[0], "Standard" + kind, i[1], i[2], i[3], i[4])
    create_single_family_house_tabula_window(i[0], "Window" + kind, i[1], i[2], i[3], i[4])
    create_single_family_house_tabula_window_adv(i[0], "WindowAdv" + kind, i[1], i[2], i[3], i[4])
    create_single_family_house_tabula_rooftop(i[0], "Rooftop" + kind, i[1], i[2], i[3], i[4])
    create_single_family_house_tabula_groundfloor(i[0], "Groundfloor" + kind, i[1], i[2], i[3], i[4])
    create_single_family_house_tabula_outerwall(i[0], "Outerwall" + kind, i[1], i[2], i[3], i[4])
"""

i = 1840


#create_single_family_house_tabula_standard(1880, "StandardRowHouse")
#create_single_family_house_tabula_standard(1925, "StandardRowHouse")
#create_single_family_house_tabula_window_adv(i, "WindowAdvRowHouse")
#create_single_family_house_tabula_rooftop(i, "RooftopRowHouse")
create_single_family_house_tabula_standard(1880, "StandardRowHouse", floors, floor_height, area, neighbours)
create_single_family_house_tabula_standard(1925, "StandardRowHouse", floors, floor_height, area, neighbours)
create_single_family_house_tabula_standard(1954, "StandardRowHouse", floors, floor_height, area, neighbours)
create_single_family_house_tabula_standard(1960, "StandardRowHouse", floors, floor_height, area, neighbours)



print(names)

prj.dir_reference_results = utilities.get_full_path(
        os.path.join(
            "examples",
            "examplefiles",
            "ReferenceResults",
            "Dymola"))

print(prj.dir_reference_results)

prj.used_library_calc = 'AixLib'
prj.number_of_elements_calc = 2
prj.merge_windows_calc = False
prj.weather_file_path = utilities.get_full_path(
        os.path.join(
            "data",
            "input",
            "inputdata",
            "weatherdata",
            "DEU_BW_Mannheim_107290_TRY2010_12_Jahr_BBSR.mos"))


prj.calc_all_buildings(raise_errors=False)

path = prj.export_aixlib(
        internal_id=None,
        path=None)
