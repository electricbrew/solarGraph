import logging
from enphase_int import EnphaseInterface

class InverterClassFactory:
    """Class for selecting an appropriate API class for various data sources."""
    def __init__(self):
        """Construct localized state."""
        self.inv_map = {}

    def register_inverter(self, inverter_type, invClass, inverter_req_params):
        """Register a recognized inverter class into the factory."""
        self.inv_map[inverter_type] = {'class': invClass, 'reqParams': inverter_req_params}

    def getInvClass(self, inverter_type, inverter_config):
        logger = logging.getLogger(__name__)
        if inverter_type not in self.inv_map:
            raise RuntimeError(f'Unknown/unsupported inverter type {inverter_type} in config file.')
        if not all([(subconf in inverter_config) for subconf in self.inv_map[inverter_type]['reqParams']]):
            err_str = 'ERROR: Settings file must satisfy all required input params for %s inverter type. %s' % \
                        (inverter_type, self.inv_map[inverter_type]['reqParams'])
            logger.error(err_str)
            raise RuntimeError(err_str)
        return self.inv_map[inverter_type]['class'](**inverter_config)


inv_factory = InverterClassFactory()

inv_factory.register_inverter('enphase_envoy', EnphaseInterface, ['site', 'user_id', 'apikey'])
