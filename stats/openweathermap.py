import requests
import logging
import time


class OpenWeatherMapAPI():
    def __init__(self, **kwargs):
        self.key = kwargs['apikey']
        self.longitude = kwargs['longitude']
        self.latitude = kwargs['latitude']
        self.units = kwargs['units'] if 'units' in kwargs else 'imperial'
        self.logger = logging.getLogger(__name__)

    def getCurrentWeather(self):
        """Call openweathermap.org API to get hourly weather data."""
        params = {
            'lat': self.latitude,
            'lon': self.longitude,
            'units': self.units,
            'exclude': 'minutely,hourly,daily,alerts',
            'appid': self.key
        }
        data = requests.get('https://api.openweathermap.org/data/2.5/onecall', params).json()
        self.logger.debug(data)
        current = data['current']
        return {'dt': current['dt'], 'temp': current['temp'], 'uvi': current['uvi'], 'clouds': current['clouds']}
