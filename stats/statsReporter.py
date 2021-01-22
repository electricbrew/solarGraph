import socket
import pickle
import struct


class StatsReporter:
    """Class to gather solar production and consumption metrics."""
    def __init__(self, logger=None):
        self.logger = logger

        self.carbonConn = socket.create_connection(('localhost', 2004))
        if self.logger:
            self.logger.debug('conn = %s', self.carbonConn)

    def send_metrics_to_db(self, metrics):
        """Store metrics in Graphite/Carbon db."""
        payload = pickle.dumps(metrics, protocol=2)
        header = struct.pack("!L", len(payload))
        message = header + payload
        if self.logger:
            self.logger.debug('Message to db: %s, length=%d', message, len(message))

        rc = self.carbonConn.send(message)
        if self.logger:
            self.logger.debug('send rc = %s', rc)
