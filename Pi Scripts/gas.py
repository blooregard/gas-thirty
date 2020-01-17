from mq import *
import sys, time
import datetime
from AzureConnect import AC

gas_lpg = []
ch4 = []
dates = []
counter = 0

try:
    print("Press CTRL+C to abort")

    mq = MQ();
    while True:
        perc = mq.MQPercentage()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        gas_lpg.append(perc["GAS_LPG"])
        ch4.append(perc["CH4"])
        dates.append(now)
        counter += 1
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write("LPG: %g ppm, CH4: %g ppm" % (perc["GAS_LPG"],perc["CH4"]))
        sys.stdout.flush()
        time.sleep(1)
        if len(dates) == 100:
            gas_dict = {'datetime':dates,'ch4':ch4,'gas_lpg':gas_lpg}
            XX = AC()
            XX.set_db('https://gas-thirty.documents.azure.com:443/',
                      'Q0ePFNbM7l6ncK9B6J1w6BrPkTahU9TuD0ZgWUAO6mpjTS65WQBuOZkES17MolYNCXtOxpfHAEvDqAwgBN6NJg==',
                      'gas-thirty')
            XX.set_container('gasdump', '/datetime')
            XX.upsert_data(gas_dict,counter)
            gas_dict.clear()
            gas_lpg = []
            ch4 = []
            dates = []
            counter = 0
            print('Gas data loaded to Azure')

except Exception as e:
    print("\nAbort by user")
