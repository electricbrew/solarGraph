import logging
from openweathermap import OpenWeatherMapAPI


class WeatherClassFactory:
    """Class for selecting an appropriate API class for various data sources."""
    def __init__(self):
        """Construct localized state."""
        self.weather_map = {}

    def register_weather_provider(self, provider, weatherClass, provider_req_params):
        """Register a recognized weather provider class into the factory."""
        self.weather_map[provider] = {'class': weatherClass, 'reqParams': provider_req_params}

    def getWeatherClass(self, provider, weather_config):
        logger = logging.getLogger(__name__)
        if provider not in self.weather_map:
            raise RuntimeError(f'Unknown/unsupported weather data provider {provider} in config file.')
        if not all([(subconf in weather_config) for subconf in self.weather_map[provider]['reqParams']]):
            err_str = 'ERROR: Settings file must satisfy all required input params for %s weather data provider. %s' % \
                        (provider, self.weather_map[provider]['reqParams'])
            logger.error(err_str)
            raise RuntimeError(err_str)
        return self.weather_map[provider]['class'](**weather_config)


weather_factory = WeatherClassFactory()

weather_factory.register_weather_provider('openweathermap.org', OpenWeatherMapAPI, ['longitude', 'latitude', 'apikey'])
