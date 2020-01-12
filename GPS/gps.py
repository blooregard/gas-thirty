from gps3 import agps3
from time import sleep

gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()
for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        print(f"Lat: {data_stream.lat}, Long: {data_stream.lon}, Alt: {data_stream.alt}")
        sleep(5)