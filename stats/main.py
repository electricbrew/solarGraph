import configparser
import time
import random
import logging
import os
from pprint import pprint
import json
from sys import exit

from inverterClassFactory import inv_factory
from weatherClassFactory import weather_factory
from statsReporter import StatsReporter


def calc_power_with_units(count, units):
    multiplier_map = {
        'Wh': 1,
        'kWh': 1000,
        'MWh': 1000000,
        'GWh': 1000000000
    }
    if units not in multiplier_map:
        raise RuntimeError('Unrecognized power units %s in output' % units)
    return count * multiplier_map[units]


LOG_LEVELS = {'INFO': logging.INFO, 'DEBUG': logging.DEBUG,
              'ERROR': logging.ERROR, 'WARNING': logging.WARNING}
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=LOG_LEVELS[LOG_LEVEL])
logger = logging.getLogger(__name__)  # pylint: disable=invalid-name

config = configparser.ConfigParser()
config.read('../settings.conf')

if 'default' in config and 'refresh' in config['default']:
    refreshInterval = int(config['default']['refresh'])
else:
    refreshInterval = 60

if not 'inverter_type' in config['default']:
    logger.error('Config file must include inverter_type in default settings')
    exit(-1)

invClass = inv_factory.getInvClass(config['default']['inverter_type'], config['inverter_settings'])

weatherClass = weather_factory.getWeatherClass(config['weather_settings']['provider'], config['weather_settings'])

stats = StatsReporter(logger)

path_prefix = 'test'
last_run = None
while True:
    try:
        t0 = int(time.time())
        data = invClass.getInverterOutput()
        cons_data = invClass.getConsumptionStats(start_at=last_run, end_at=t0)
        weather_data = weatherClass.getCurrentWeather()

        if not last_run:
            pprint(data)
        last_run = t0

        metrics = [
            (path_prefix + '.weather' + '.temp', (weather_data['dt'], weather_data['temp'])),
            (path_prefix + '.weather' + '.uvi', (weather_data['dt'], weather_data['uvi'])),
            (path_prefix + '.weather' + '.clouds', (weather_data['dt'], weather_data['clouds']))
        ]
        print(metrics)
        stats.send_metrics_to_db(metrics) 

        for system in data:
            for micro_inverter in system['micro_inverters']:
                inverter_path = '.'.join([path_prefix, micro_inverter['envoy_serial_number'], micro_inverter['serial_number']])
                metrics = [
                    (inverter_path + '.inst_power', (t0, micro_inverter['power_produced'])),
                    (inverter_path + '.lifetime_power', (t0, calc_power_with_units(micro_inverter['energy']['value'], micro_inverter['energy']['units']))),
                    (inverter_path + '.status', (t0, micro_inverter['status']))
                ]
                print(metrics)
                stats.send_metrics_to_db(metrics)    

        if 'intervals' in cons_data:
            for interval in cons_data['intervals']:
                metrics = [
                    # 15 min intervals, so multiply by 4 to get avg usage from Wh
                    ('.'.join([path_prefix, 'inst_usage']), (interval['end_at'], interval['enwh'] * 4))
                ]
                print(metrics)
                stats.send_metrics_to_db(metrics)

        time.sleep(refreshInterval)

    except Exception:  # pylint: disable=broad-except
        pass
