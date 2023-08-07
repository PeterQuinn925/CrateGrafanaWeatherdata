#!/usr/bin/python3
#fuzzy sine wave simulated demo data
#https://rockwellautomation.atlassian.net/wiki/spaces/POMTARDIS/pages/3271688962/Jupyter+Notebook+configuration+with+FTDM   
import datetime
import time
import math
import random

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.data_classes import TimeSeries

host = "https://westeurope-1.cognitedata.com"
myproject = "rok-buandcollaborators-53"
clientid = "HXoBmEbgNkabcE17x1mAiYSaxyzoCa9i"
secret = "TRoPillseuCknmcJlF6HfoobargFgoWorogluVKzagUR-BztIZeokZlgztxyzKDtgNR"
#myscope = "https://westeurope-1.cognitedata.com/.default"
myscope='["IDENTITY", "user_impersonation"]'
token="https://datamosaix-prod.us.auth0.com/oauth/token"
dataset = 8883655420989208 #chemdemo dataset

#creds = OAuthClientCredentials(token_url=token,client_id=clientid, client_secret=secret, scopes=myscope)
#cnf = ClientConfig(client_name="SJC_Raspi3b", base_url=host, project=myproject, credentials=creds)
creds = OAuthClientCredentials(
        token_url=token, # https://datamosaix-qa.us.auth0.com/oauth/token
        client_id=clientid,
        client_secret=secret,
        scopes=["IDENTITY", "user_impersonation"]
)

cnf = ClientConfig(
    client_name="SJC_Raspi3b",
    project=myproject,
    credentials=creds,
    base_url=host
)

cdf_client = CogniteClient(cnf)

#ts_list = cdf_client.time_series.list() #debugging test for creds. not needed for real
#print (ts_list)


def sendCDF(tsname,tsvalue):  
    timestamp = int(time.time())
    #see if there is a cognite timeseries for this value
    res = cdf_client.time_series.search(name=tsname)
    if len(res)>0 and res[0].name==tsname:
        ts = res[0]
    else:
        #doesn't exist yet, add it
        ts = cdf_client.time_series.create(TimeSeries(name=tsname, data_set_id=dataset, external_id=tsname))
    datapoint = [(timestamp*1000,tsvalue)]
    cdf_client.time_series.data.insert(datapoint, id = ts.id)

       
 # generate data
tseries = [{"name": 'TK-40201-TT', "scale":40, "offset":200, "fuzz":20, "shift":0,"speed":1}]
tseries.append({"name": 'TK-10201-PT', "scale":40,"offset":200, "fuzz":20, "shift":0,"speed":1.5})
tseries.append({"name": 'TK-10201-LT', "scale":30, "offset":45,"fuzz":10, "shift":10,"speed":1})
tseries.append({"name": 'TK-10201-TT', "scale":20,"offset":200, "fuzz":10, "shift":0,"speed":1.5})
tseries.append({"name": 'TK-40201-PT', "scale":40,"offset":200, "fuzz":20, "shift":0,"speed":1.5})
tseries.append({"name": 'TK-40201-LT', "scale":20, "offset":45,"fuzz":30, "shift":10,"speed":1})
tseries.append({"name": 'TK-40101-TT', "scale":50,"offset":180, "fuzz":10, "shift":0,"speed":1.5})
tseries.append({"name": 'TK-40101-LT', "scale":20,"offset":45,"fuzz":10, "shift":20,"speed":1})
tseries.append({"name": 'P-40201-FT', "scale":3,"offset":10, "fuzz":15, "shift":5,"speed":1.1})
tseries.append({"name": 'P-10201-FT', "scale":4,"offset":10,"fuzz":15, "shift":5,"speed":2})
i=0
while True:
    for deg in range (0,360,10):
        for ts in tseries:
            fuzz = random.random()*ts['fuzz']
            tsname = ts['name']
            #print (ts['scale'])
            tsval = math.sin(math.radians(deg+ts['shift']*ts['speed']))*ts['scale']+ts['offset']+fuzz
            print (tsname,deg+ts['shift'],tsval,fuzz)
            sendCDF(tsname,tsval)
        time.sleep(120) #every 2 minutes     
