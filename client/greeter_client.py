import requests
from flask import Flask, request
from configparser import ConfigParser
import grpc
import GreetingService_pb2
import GreetingService_pb2_grpc

parser = ConfigParser()
parser.read("settings.ini")

app = Flask(__name__)

@app.route('/v1/forecast/city')
def forecast():

    with grpc.insecure_channel('localhost:50052') as channel:
        stub = GreetingService_pb2_grpc.GreeterStub(channel)
        response = stub.sayHello(GreetingService_pb2.Request(name=request.headers.get('Own-Auth-UserName')))
        print(f'{response.message}')
        if response.message != 'True':
            return '403 Forbidden Error'

    city = request.args.get('q')
    responsez = requests.get(parser.get("API", 'weather'),
                             params={'q': city, 'appid': parser.get('token', 'open_weather_token'),
                                     'units': 'metric'}).json()
    if responsez.get("cod") != 200:
        message = responsez.get('message', '')
        return f'Город {city.title()} не найден на карте.'
    idid = responsez["id"]

    response = requests.get(parser.get('API', 'fore'),
                            params={'id': idid, 'appid': parser.get('token', 'open_weather_token'), 'units': 'metric'})
    data = response.json()

    forecast_temperature = data.get('list', [{}])
    if not forecast_temperature:
        return f'Ошибка получения погоды для города {city.title()}'
    else:
        return data


@app.route('/v1/current/city')
def current():

    with grpc.insecure_channel('localhost:50052') as channel:
        stub = GreetingService_pb2_grpc.GreeterStub(channel)
        response = stub.sayHello(GreetingService_pb2.Request(name=request.headers.get('Own-Auth-UserName')))
        print(f'{response.message}')
        if response.message != 'True':
            return '403 Forbidden Error'

    city = request.args.get('q')
    response = requests.get(parser.get('API', 'weather'),
                            params={'q': city, 'appid': parser.get('token', 'open_weather_token'), 'units': 'metric'})
    data = response.json()
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


