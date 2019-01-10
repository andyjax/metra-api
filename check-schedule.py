import json
import sys
import requests
import urllib3
#import ssl
#from io import StringIO, BytesIO

def ProgramMain():
    urllib3.disable_warnings()
    with open('trip-ids.json') as trips:
        tripsJson=json.load(trips)

#    global apiCred
#    global accessKey
#    global secretKey
#    global j

    with open('credential.json') as creds:
        apiCred=json.load(creds)
    
#    accessKey = apiCred['accessKey']
#    secretKey = apiCred['secretKey']
    authKey = apiCred['authorization']

#    print "accessKey: {0}, secretKey: {1}".format(accessKey, secretKey)
    print("Morning Trip ID's to look for:")
    for j in tripsJson['morning']:
        print("{0}".format(j['trip_id']))

    url = "https://gtfsapi.metrarail.com/gtfs/tripUpdates"

    payload = ""
    headers = {
        'Authorization': authKey,
        'cache-control': "no-cache"
    }

    response = requests.request("GET", url, data=payload, headers=headers)

    for morningTrip in tripsJson['morning']:
        for i in response.json():
            if (morningTrip['trip_id']==i['id']):
                delay = float(i['trip_update']['stop_time_update'][0]['arrival']['delay'])/60
                print("{0} exists! Delay is: {1} minutes".format(morningTrip['trip_id'], delay))

#    for i in response.json():
#        if (i['id']=="UP-NW_UNW619_V1_B"):
#            print "UP-NW_UNW619_V1_B exists!"
#        print "id: {0}".format(i['id'])

#    print "Trip Updates:"
#    print(response.json()[1]['id'])

ProgramMain()