import requests
import os
import copy
import gpxpy

valhalla_url = 'http://{}:{}/route'

mode_conversion = {'car': 'auto',
                   'foot': 'pedestrian',
                   'bike': 'bicycle'}

pr = None

def init(registry):
    global pr
    global valhalla_url
    pr = registry
    valhalla_ip = os.environ.get('VALHALLA_IP', '127.0.0.1')
    valhalla_port = os.environ.get('VALHALLA_PORT', '8002')
    valhalla_url = valhalla_url.format(valhalla_ip, valhalla_port)
    registry.register_plugin('car',
                             {'router': lambda x,y: find_path(x,y,'car'),
                              'id': 'valhalla_car',
                              'desc': 'Car routing with valhalla'})
    print('Registered valhalla car routing plugin')
    registry.register_plugin('foot',
                             {'router': lambda x,y: find_path(x,y,'foot'),
                              'id': 'valhalla_foot',
                              'desc': 'Foot routing with valhalla'})
    print('Registered valhalla foot routing plugin')
    registry.register_plugin('bike',
                             {'router': lambda x,y: find_path(x,y,'bike'),
                              'id': 'valhalla_bike',
                              'desc': 'Bike routing with valhalla'})
    print('Registered valhalla bike routing plugin')

route_request_template = {"locations": [],
                          "costing":"auto",
                          "directions_options": {"units":"km",
                                                 "format": "gpx"}
                        }

"""
find_path - find path via the the valhalla server
returns a gpx with the route specified

Parameters:
coord_begin - tuple (latitude, longitude)
coord_end - tuple (latitude, longitude)
mode - can be either 'car', 'foot', 'bike'
"""
def find_path(coord_begin, coord_end, mode):
    route_request = copy.deepcopy(route_request_template)
    route_request['locations'] = [{'lat': coord_begin[0],
                                   'lon': coord_begin[1]},
                                  {'lat': coord_end[0],
                                   'lon': coord_end[1]}]
    if mode in mode_conversion:
        route_request['costing'] = mode_conversion[mode]
    else:
        route_request['costing'] = mode
    request = requests.post(valhalla_url, json = route_request)
    path = request.text
    route_request['directions_options']['format'] = 'json'
    request_data = requests.post(valhalla_url, json = route_request)
    if request.status_code == 200:
        return pr.get_route().route(coord_begin, coord_end, mode,
                                    request_data.json()['trip']['summary']['time'],
                                    request_data.json()['trip']['summary']['length'],
                                    gpxpy.parse(request.text).routes[0])
    else:
       return None
