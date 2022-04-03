import requests
import datetime
from flask import Flask, request
from configparser import ConfigParser

parser = ConfigParser()
parser.read("settings.ini")

app = Flask(__name__)


@app.route('/v1/forecast/city')
def forecast():
    city = request.args.get('q')

    responsez = requests.get(parser.get("API", 'weather'),
                             params={'q': city, 'appid': parser.get('token', 'open_weather_token'),
                                     'units': 'metric'}).json()
    if responsez.get("cod") != 200:
        message = responsez.get('message', '')
        return f'Город {city.title()} не найден на карте.'
    idid = responsez["id"]

    response = requests.get(parser.get('API', 'fore'),
                            params={'id': idid, 'appid': parser.get('token', 'open_weather_token'), 'units': 'metric'}
                            )
    data = response.json()

    forecast_temperature = data.get('list', [{}])
    if not forecast_temperature:
        return f'Ошибка получения погоды для города {city.title()}'
    else:
        return data


@app.route('/v1/current/city')
def current():
    # API_KEY = 'e5a734b092732dadf1c0ae549afeb79f'
    city = request.args.get('q')

    response = requests.get(parser.get('API', 'weather'),
                            params={'q': city, 'appid': parser.get('token', 'open_weather_token'), 'units': 'metric'})
    data = response.json()

    # error like unknown city name, inavalid api key
    if data.get('cod') != 200:
        message = data.get('message', '')
        return f'Город {city.title()} не найден на карте.'

    current_temperature = data.get('main', {}).get('temp')

    if not current_temperature:
        return f'Ошибка получения погоды для города {city.title()}'
    else:
        return data

if __name__ == '__main__':
    app.run(host=parser.get('connect', 'ip'),port = parser.get('connect', 'port'), debug=True)
