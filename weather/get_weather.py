#!/usr/bin/env python3

import sys
import json
import argparse
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError

def parse_args():
    parser = argparse.ArgumentParser(description='Print weather data from OpenWeatherMap.org')
    parser.add_argument('-k', '--key', required=True, help='API Key')
    parser.add_argument('-z', '--zip', type=int, required=True, help='Zip code')
    parser.add_argument('-c', '--country', default='us', help='Country code for zip (default: "us")')
    args = parser.parse_args()
    return args

def format_weather_message(json_data):
    message = '{} deg'.format(int(json_data['main']['temp']))
    message += ', {}% humidity'.format(int(json_data['main']['humidity']))
    message += ', {} hPa'.format(int(json_data['main']['pressure']))
    message += ', {}'.format(get_wind(json_data))
    message += ', {}'.format(json_data['weather'][0]['description'])
    return message

def get_wind(json_data):
    wind = '{} mph {}'.format(
        int(json_data['wind']['speed']), 
        deg_to_compass(json_data['wind']['deg'])
    )
    return wind

def deg_to_compass(num):
    val=int((num/22.5)+.5)
    arr=["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
    return arr[(val % 16)]

def main():

    WEATHER_API_URL='https://api.openweathermap.org/data/2.5/weather'
    args = parse_args()
    params = {
        # 'q': 'Philadelphia',
        'zip': '{},{}'.format(args.zip, args.country),
        'appid': args.key,
        'units': 'imperial'
    }

    try:
        response = urlopen('{}?{}'.format(WEATHER_API_URL, urlencode(params)))
    except HTTPError as err:
        if err.code == 401:
            print('Unauthorized. Invalid API key: {}'.format(params['appid']))
        else:
            print('{} {}'.format(err.code, err.reason), file=sys.stderr)
        sys.exit(1)

    if response.code == 200:
        try:
            data = json.loads(response.read().decode('utf8'))
        except:
            print('Error interpretting HTTP response as JSON.', file=sys.stderr)
            sys.exit(1)
        print(format_weather_message(data))


if __name__ == '__main__':
    main()
