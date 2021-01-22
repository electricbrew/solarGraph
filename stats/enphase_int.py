
import requests
import logging


class EnphaseInterface:
    """Wrapper class for interfacing with Enphase API."""
    def __init__(self, **kwargs):
        """Constructor to latch state needed for API and logging."""
        self.site = kwargs['site']
        self.user_id = kwargs['user_id']
        self.key = kwargs['apikey']
        self.logger = logging.getLogger(__name__)

    def checkEnvoyStatus(self):
        """Check status of all envoys in the system."""
        status = {}
        payload = {
            'user_id': self.user_id,
            'key': self.key
        }
        data = requests.get(f'https://api.enphaseenergy.com/api/v2/systems/{self.site}/envoys', params=payload).json()
        self.logger.info(data)
        print(data)
        for envoy in data['envoys']:
            status[envoy['envoy_id']] = {'status': envoy['status'], 'last_reported': envoy['last_report_at']}
        return status

    def getInverterOutput(self):
        """Get production output of inverters in the system."""
        payload = {
            'site_id': self.site,
            'user_id': self.user_id,
            'key': self.key
        }
        data = requests.get('https://api.enphaseenergy.com/api/v2/systems/inverters_summary_by_envoy_or_site', params=payload).json()
        self.logger.info(data)
        return data

    def getConsumptionStats(self, start_at=None, end_at=None):
        """Get consumption stats if available from envoy."""
        payload = {
            'user_id': self.user_id,
            'key': self.key
        }
        if start_at:
            payload['start_at'] = start_at
        if end_at:
            payload['end_at'] = end_at
        data = requests.get(f'https://api.enphaseenergy.com/api/v2/systems/{self.site}/consumption_stats', params=payload).json()
        self.logger.info(data)
        return data

    def getRGMStats(self, start_at=None, end_at=None):
        """Get revenue grade meter statistics."""
        payload = {
            'user_id': self.user_id,
            'key': self.key
        }
        if start_at:
            payload['start_at'] = start_at
        if end_at:
            payload['end_at'] = end_at
        data = requests.get(f'https://api.enphaseenergy.com/api/v2/systems/{self.site}/rgm_stats', params=payload).json()
        self.logger.info(data)
        return data
