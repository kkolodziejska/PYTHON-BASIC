import json
import os
from pprint import pprint

DIRECTORY_PATH = "source_data"
CITY = 'Barcelona'
FILENAME = '2021_09_25.json'
FILE_PATH = os.path.join(DIRECTORY_PATH, CITY, FILENAME)


with open(FILE_PATH, 'r') as f:
    barcelona_data = json.load(f)

all_temp = [hour['temp'] for hour in barcelona_data['hourly']]
all_winds = [hour['wind_speed'] for hour in barcelona_data['hourly']]

mean_temp = sum(all_temp) / len(all_temp)
max_temp = max(all_temp)
min_temp = min(all_temp)
mean_wind = sum(all_winds) / len(all_winds)
max_wind = max(all_winds)
min_wind = min(all_winds)

print('TEMP: ', mean_temp, max_temp, min_temp)
print('WIND: ', mean_wind, max_wind, min_wind)
