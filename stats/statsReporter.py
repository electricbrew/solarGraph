import socket
import pickle
import datetime
import struct

path1 = 'test.metric1'
path2 = 'test.metric2'

metrics = [(path1, (datetime.datetime.now(), 1)), (path2, (datetime.datetime.now(), 2))]

payload = pickle.dumps(metrics, protocol=2)
header = struct.pack("!L", len(payload))
message = header + payload
print(f'message = {message}')

carbonConn = socket.create_connection(('localhost', 2004))
print(f'conn = {carbonConn}')

rc = carbonConn.send(message)
print(f'send rc = {rc}')
