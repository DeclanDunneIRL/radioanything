from flask import Flask, jsonify, render_template
import schedule
import time
import random

from pyradios import RadioBrowser
from werkzeug.routing import BaseConverter

class ListConverter(BaseConverter):
    def to_python(self, value):
        return value.split(',')
    
    def to_url(self, values):
        return ','.join(BaseConverter.to_url(value) for value in values)

app = Flask(__name__)
app.url_map.converters['list'] = ListConverter

# Update a station cache every 24 hours or on startup
def update_stations():
    global stations
    global stationCount
    rb = RadioBrowser()
    stations = rb.stations()
    stationCount = len(stations)
    print("Updated stations")

# Update a station cache every 24 hours
schedule.every(24).hours.do(update_stations)
update_stations()

# Get a random station from the cache
def random_station():
    # Pick a number between 0 and the number of stations then return that station
    return stations[random.randint(0, stationCount - 1)]

# Get a station from the cache by stationuuid
def get_station(stationuuid):
    # Find the station in the cache and return it
    for station in stations:
        if station['stationuuid'] == stationuuid:
            return station

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/random_station', methods=['GET'])
def fetch_random_station():
    station = random_station()
    return jsonify(station), 200

@app.route('/station/<string:stationuuid>', methods=['GET'])
def fetch_station(stationuuid):
    station = get_station(stationuuid)
    if station is None:
        return jsonify({'error': 'Station not found'}), 404
    return jsonify(station), 200

@app.route('/play/<string:stationuuid>', methods=['GET'])
def play_station(stationuuid):
    station = get_station(stationuuid)
    if station is None:
        return jsonify({'error': 'Station not found'}), 404
    return render_template('index.html', stationuuid=stationuuid)

if __name__ == '__main__':
    app.run(debug=True)