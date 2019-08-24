
import json
import argparse
import logging
import sys
import os
from random import randint

import carla
from cexp.env.server_manager import start_test_server, check_test_server



from cexp.env.utils.route_configuration_parser import \
        parse_annotations_file, parse_routes_file, scan_route_for_scenarios

from srunner.challenge.utils.route_manipulation import interpolate_trajectory




def get_scenario_list(world, scenarios_json_path, routes_path):

    world_annotations = parse_annotations_file(scenarios_json_path)

    route_descriptions_list = parse_routes_file(routes_path)

    per_route_possible_scenarios = []
    for route in route_descriptions_list:

        _, route_interpolated = interpolate_trajectory(world, route['trajectory'])

        possible_scenarios, existent_triggers = scan_route_for_scenarios(route_interpolated,
                                                                         world_annotations,
                                                                         world.get_map().name)
        per_route_possible_scenarios.append(possible_scenarios)


    return route_descriptions_list, per_route_possible_scenarios



# TODO pregenerate the names

def generate_json_with_scenarios(world, scenarios_json_path, routes_path,
                                 wanted_scenarios, output_json_name,
                                 number_of_routes=200):

    """

    :param world:
    :param scenarios_json_path:
    :param routes_path:
    :param wanted_scenarios:
    :param output_json_name:
    :param number_of_routes: the number of routes used on the generation
    :return:
    """








    routes_parser, possible_scenarios = get_scenario_list(world, scenarios_json_path, routes_path)


    weather_sets = {'training': ["ClearNoon",
                                  "WetNoon",
                                  "HardRainNoon",
                                   "ClearSunset"]
                    }
    new_json = {"envs": {},
                "package_name": output_json_name,

                }

    for w_set_name in weather_sets.keys():
        # get the actual set  from th name
        w_set = weather_sets[w_set_name]

        for weather in w_set:

            for route in routes_parser[]:
                #for town_name in town_sets.keys():

                for env_number in range(200):
                    env_dict = {
                        "route": {
                            "file": routes_path,
                            "id": randint(0, 65790)
                        },
                        "scenarios": {"file": "None",
                                      'background_activity': {"vehicle.*": 100,
                                                              "walker.*": 0}
                                      },
                        "town_name": "Town01",
                        "vehicle_model": "vehicle.lincoln.mkz2017",
                        "weather_profile": weather
                    }

                    new_json["envs"].update({weather + '_' + town_sets[town_name] + '_route'
                                             + str(env_number).zfill(5): env_dict})






    """



    root_route_file_position = 'database/corl2017'
    root_route_file_output = 'database'
    # root_route_file_position = 'srunner/challenge/'
    #filename_town01 = os.path.join(root_route_file_position, 'Town01_navigation.json')

    # The sensor information should be on get data


    # For each of the routes to be evaluated.

    # Tows to be generated
    town_sets = {
                 'routes/routes_all.xml': 'routes'
                 }


    # Weathers to be generated later
    weather_sets = {'training': ["ClearNoon",
                                  "WetNoon",
                                  "HardRainNoon",
                                   "ClearSunset"]
                    }



    new_json = {"envs": {},
                "package_name": 'dataset_vehicles_l1',

                }

    for w_set_name in weather_sets.keys():
        # get the actual set  from th name
        w_set = weather_sets[w_set_name]

        for weather in w_set:

            for town_name in town_sets.keys():

                for env_number in range(200):

                    env_dict = {
                        "route": {
                            "file": town_name,
                            "id": randint(0,65790)
                        },
                        "scenarios": {"file": "None",
                                      'background_activity': {"vehicle.*": 100,
                                                              "walker.*": 0}
                                      },
                        "town_name": "Town01",
                        "vehicle_model": "vehicle.lincoln.mkz2017",
                        "weather_profile": weather
                    }

                    new_json["envs"].update({weather + '_' + town_sets[town_name] + '_route'
                                             + str(env_number).zfill(5): env_dict})

    filename = os.path.join(root_route_file_output, 'dataset_vehicles_l1.json')

    with open(filename, 'w') as fo:
        # with open(os.path.join(root_route_file_position, 'all_towns_traffic_scenarios3_4.json'), 'w') as fo:
        fo.write(json.dumps(new_json, sort_keys=True, indent=4))

    """


if __name__ == '__main__':
    description = ("CARLA AD Challenge evaluation: evaluate your Agent in CARLA scenarios\n")

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-t', '--town', default='Town01', help='The town name to be used')

    parser.add_argument('-o', '--output', default='database/dataset_scenarios_l0.json',
                        help='The outputfile json')



    parser.add_argument('-r', '--input-route', default='database/routes/routes_town01.xml',
                        help='The outputfile json')


    parser.add_argument('-j', '--scenarios-json',
                        default='database/scenarios/all_towns_traffic_scenarios1_3_4.json',
                        help='the input json with scnarios')

    arguments = parser.parse_args()

    if not check_test_server(6666):
        start_test_server(6666)
        print (" WAITING FOR DOCKER TO BE STARTED")

    client = carla.Client('localhost', 6666)

    world = client.load_world(arguments.town)

    generate_json_with_scenarios(world, arguments.scenarios_json, arguments.input_route,
                                 wanted_scenarios=['Scenario3', 'Scenario4'])