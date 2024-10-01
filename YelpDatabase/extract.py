import requests
import json
import numpy as np
import sys
import haversine as hs

from util.constants import YELPKEY

url = 'https://api.yelp.com/v3/businesses/search'

headers = {
    'Authorization': f'Bearer {YELPKEY}'
}

params = {
    'latitude': 49.2818,
    'longitude': -123.1226,
    'categories': 'restaurants',
    'limit': 40,                       
    'offset': 0,                        
    'radius': 100,                     
}

def generate_center_points_radius(lat_low, lat_high, long_low, long_high, steps):

    grid_lat = np.linspace(lat_low, lat_high, num=steps)
    grid_long = np.linspace(long_low, long_high, num=steps)
    box_points = []
    radius = 0
    for i in range(steps-1):
        for j in range(steps-1):
            radius = max(radius, hs.haversine((grid_lat[i], grid_long[j]), (grid_lat[i+1], grid_long[j+1]), unit=hs.Unit.METERS))
            box_points.append([grid_lat[i], grid_lat[i+1], grid_long[j], grid_long[j+1]])
    return box_points, int(radius/1.4)

def get_restaurants(lat, long, offset, radius):

    params['latitude'] = lat
    params['longitude'] = long
    params['offset'] = offset
    params['radius'] = radius
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error: {response.status_code}')
        return None

def get_grid_restaurants(lat_low, lat_high, long_low, long_high, radius):

    restaurants = []
    lat = np.round((lat_low+lat_high)/2, 6)
    long = np.round((long_low+long_high)/2, 6)
    offset = 0
    params['offset'] = 0
    params['limit'] = 50
    params['latitude'] = lat
    params['longitude'] = long
    params['radius'] = radius
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'Error: {response.status_code}')
        print(f'Total restaurants fetched:{len(restaurants)}')
    else:
        data = response.json()
        if(data=={} or data==None):
            print(f"Not fetched any restaurant in this grid: [{lat_low}, {lat_high}, {long_low}, {long_high}]")
        else:
            total = data['total']
            print(f'found {total} restaurants in this grid [{lat_low}, {lat_high}, {long_low}, {long_high}], fetching ')
            if(total <= 50):
                restaurants.extend(data['businesses']) 
                print(f'Fetched {len(data["businesses"])} restaurants in this grid: [{lat_low}, {lat_high}, {long_low}, {long_high}],\
                        Total so far: {len(restaurants)}')
            elif(total <= 240):
                while(offset<total):
                    params['limit'] = 40
                    data = get_restaurants(lat, long, offset, radius)
                    restaurants.extend(data['businesses']) 
                    print(f'Fetched {len(data["businesses"])} restaurants, Total so far: {len(restaurants)}')
                    offset +=40
            else:
                print(f'Too many businesses in this grid: {total}, need to divide the grid: [{lat_low}, {lat_high}, {long_low}, {long_high}]')
                box_points, radius = generate_center_points_radius(lat_low, lat_high, long_low, long_high, 5)
                for (lat_low, lat_high, long_low, long_high) in box_points:
                    restaurants.extend(get_grid_restaurants(lat_low, lat_high, long_low, long_high, radius))
    return restaurants
    

def get_all_restaurants():

    lat_low, lat_high, long_low, long_high = (49.002, 49.494, -123.340, -122.313)
    box_points, radius = generate_center_points_radius(lat_low, lat_high, long_low, long_high, 10)
    total_restaurants = 0
    
    for i in range(len(box_points)):
        (lat_low, lat_high, long_low, long_high) = box_points[i]
        grid_restaurants = get_grid_restaurants(lat_low, lat_high, long_low, long_high, radius)
        total_restaurants += len(grid_restaurants) 
        print(f'Fetched for grid {i}, {len(grid_restaurants)} restaurants; Total so far: {total_restaurants}')
        with open(f'restaurants\\vancouver_restaurants_{i}.json', 'w') as f:
            json.dump(grid_restaurants, f, indent=2)


get_all_restaurants()