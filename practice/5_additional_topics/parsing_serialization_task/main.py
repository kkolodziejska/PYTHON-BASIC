import json
import os
from lxml import etree


def get_city_data(file: str) -> dict:

    with open(file, 'r') as f:
        all_city_data = json.load(f)

    all_temp = [hour['temp'] for hour in all_city_data['hourly']]
    all_winds = [hour['wind_speed'] for hour in all_city_data['hourly']]

    city_data = {
        'mean_temp': sum(all_temp) / len(all_temp),
        'max_temp': max(all_temp),
        'min_temp': min(all_temp),
        'mean_wind_speed': sum(all_winds) / len(all_winds),
        'max_wind_speed': max(all_winds),
        'min_wind_speed': min(all_winds),
    }
    return city_data


def get_country_data(dir_path: str = 'source_data') -> dict:
    country_data = dict()

    for root, _, files in os.walk(dir_path):
        for filename in files:
            city_name = os.path.basename(root)
            file_path = os.path.join(root, filename)
            country_data[city_name] = get_city_data(file_path)

    return country_data


def get_country_summary(country_data: dict) -> dict:
    country_summary = {
        'warmest_place': max(country_data,
                             key=lambda city: country_data[city]['mean_temp']),
        'coldest_place': min(country_data,
                             key=lambda city: country_data[city]['mean_temp']),
        'windiest_place': max(country_data,
                              key=lambda city: country_data[city]['mean_wind_speed']),
        'mean_temp': sum(country_data[city]['mean_temp']
                         for city in country_data) / len(country_data),
        'mean_wind': sum(country_data[city]['mean_wind_speed']
                         for city in country_data) / len(country_data)
    }
    return country_summary


def create_country_xml(country_data: dict, country: str = 'Spain',
                       date: str = '2021-09-25'):

    country_summary = get_country_summary(country_data)

    root = etree.Element("weather", country=country, date=date)
    summary = etree.SubElement(root, "summary",
                               mean_temp=f"{country_summary['mean_temp']:.2f}",
                               mean_wind_speed=
                               f"{country_summary['mean_wind']:.2f}",
                               coldest_place=country_summary['coldest_place'],
                               warmest_place=country_summary['warmest_place'],
                               windiest_place=country_summary['windiest_place']
                               )
    cities = etree.SubElement(root, "cities")
    for city, city_data in country_data.items():
        child_city = etree.SubElement(cities, city.replace(' ', '_'))
        for key, value in city_data.items():
            child_city.set(key, f"{value:.2f}")

    with open('output.xml', 'bw') as f:
        f.write(etree.tostring(root, pretty_print=True))


if __name__ == '__main__':
    spain_data = get_country_data()
    create_country_xml(spain_data)
