import json
import sys
import requests
import urllib3
import datetime

if len(sys.argv) == 2:
    tripInput = sys.argv[1]
    try:
        numTrips = int(tripInput)
    except ValueError:
        print("Trip count must be an integer!")
        sys.exit(2)
    if (numTrips <= 0):
        print("Trip count must be greater than 0!")
        sys.exit(2)
else:
    numTrips = -1

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

# identify UP-NW trips

for i in response.json():
    if numTrips == 0:
        break
    if (i['route_id']=="UP-NW" and i['direction_id']==0 and i['service_id']=="A1"):
        # UP-NW outbound, get trip stops to see if it stops at Mount Prospect
        tripId = i['trip_id']
        stopUrl = "https://gtfsapi.metrarail.com/gtfs/schedule/stop_times/" + tripId
        stops = requests.request("GET", stopUrl, data=payload, headers=headers)
        for j in stops.json():
            if (j['stop_id']=="MTPROSPECT"):
                tripTime = stops.json()[0]['departure_time'].split(':')
                tripHour = int(tripTime[0])
                # This next part breaks trips leaving after midnight (they won't show up)
                if (tripHour == 24):
                    tripHour=0
                if (tripHour >= currentHour):
                    print("Trip {0}, departs OTC at {1}, arrives Mount Prospect at {2}".format(tripId, stops.json()[0]['departure_time'], j['arrival_time']))
                    numTrips -= 1

