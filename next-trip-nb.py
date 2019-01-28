import json
import sys
import requests
import urllib3
import datetime

urllib3.disable_warnings()
with open('credential.json') as creds:
    apiCred = json.load(creds)

authKey = apiCred['authorization']

tripUrl = "https://gtfsapi.metrarail.com/gtfs/schedule/trips"

payload = ""
headers = {
    'Authorization': authKey,
    'cache-control': "no-cache"
}

currentHour = int(datetime.datetime.now().hour)
response = requests.request("GET", tripUrl, data=payload, headers=headers)

# identify UP-N trips

for i in response.json():
    if (i['route_id']=="UP-N" and i['direction_id']==0 and i['service_id']=="A1"):
        # UP-N northbound, get trip stops to see if it stops at Central
        tripId = i['trip_id']
        stopUrl = "https://gtfsapi.metrarail.com/gtfs/schedule/stop_times/" + tripId
        stops = requests.request("GET", stopUrl, data=payload, headers=headers)
        for j in stops.json():
            if (j['stop_id']=="CENTRALST"):
                tripTime = stops.json()[0]['departure_time'].split(':')
                tripHour = int(tripTime[0])
                if (tripHour >= currentHour):
                    print("Trip {0}, departs OTC at {1}".format(tripId, stops.json()[0]['departure_time']))

# testUrl = "https://gtfsapi.metrarail.com/gtfs/schedule/stop_times/UP-N_UN314_V1_A"
# testStop = requests.request("GET", testUrl, data=payload, headers=headers)