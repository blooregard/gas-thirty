from gps3 import agps3
from time import sleep
import datetime
from AzureConnect import AC

gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()
gps_socket.connect()
gps_socket.watch()

lats = []
long = []
alt = []
dates = []
counter = 0

for new _data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        print("Lat: %s, Long: %s, Alt: %s" % (data_stream.lat, data_stream.lon, data_stream.alt))
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lats.append(data_stream.lat)
        long.append(data_stream.lon)
        alt.append(data_stream.alt)
        dates.append(now)
        counter += 1
        sleep(1)
        if len(dates) == 100:
            gps_dict = {'latitude': lats, 'longitude': long, 'altitude': alt, 'datetime': dates}
            XX = AC()
            XX.set_db('https://gas-thirty.documents.azure.com:443/',
                      'Q0ePFNbM7l6ncK9B6J1w6BrPkTahU9TuD0ZgWUAO6mpjTS65WQBuOZkES17MolYNCXtOxpfHAEvDqAwgBN6NJg==',
                      'gas-thirty')
            XX.set_container('gpsdump', '/datetime')
            XX.upsert_data(gps_dict,counter)
            gps_dict.clear()
            lats = []
            long = []
            alt = []
            dates = []
            counter = 0
            print('GPS Loaded to Azure')