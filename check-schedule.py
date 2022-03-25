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

#   populate central st arrival times

    payload = ""
    headers = {
        'Authorization': authKey,
        'cache-control': "no-cache"
    }

    url = "https://gtfsapi.metrarail.com/gtfs/tripUpdates"
    tripUpdates_response = requests.request("GET", url, data=payload, headers=headers)

    val = 0
    while (not (val=="1" or val=="2")):
        val = input("Select time period (1 - morning; 2 - evening): ")


    if (val=="1"):
        time='morning'
    elif (val=="2"):
        time='evening'
#    print("Morning Trip ID's to look for:")
    for j in tripsJson[time]:
        print("{0}".format(j['trip_id']))
        api_schedule = [j['trip_id']+"_A", j['trip_id']+"_AA", j['trip_id']+"_B", j['trip_id']+"_C", j['trip_id']+"_D"]
        printed = 0
        otc_printed = 0
        exists_printed = 0
        for k in api_schedule:
            url = "https://gtfsapi.metrarail.com/gtfs/schedule/stop_times/" + k
            response = requests.request("GET", url, data=payload, headers=headers)
#        url = "https://gtfsapi.metrarail.com/gtfs/schedule/stop_times/" + j['trip_id']
#        response = requests.request("GET", url, data=payload, headers=headers)
            for i in response.json():
                if (i['stop_id']=="MTPROSPECT" and printed==0):
                    print("\tScheduled Mount Prospect at {0}".format(i['arrival_time']))
                    printed = 1
                    if (i['center_boarding']==1):
                        print('\033[93m' + "\tBoards from center platform!".format(j['trip_id']) + '\033[0m')
                if (i['stop_id']=="OTC" and otc_printed==0):
                    print("\tScheduled OTC at {0}".format(i['arrival_time']))
                    otc_printed = 1
            for i in tripUpdates_response.json():
                if (k==i['id'] and exists_printed==0):
                    delay = float(i['trip_update']['stop_time_update'][0]['arrival']['delay'])/60
                    print('\033[1m' + "\t{0} exists! Delay is: {1} minutes".format(j['trip_id'], delay) + '\033[0m')
                    exists_printed = 1

#    for morningTrip in tripsJson['morning']:
#        for i in response.json():
#            if (morningTrip['trip_id']==i['id']):
#                delay = float(i['trip_update']['stop_time_update'][0]['arrival']['delay'])/60
#                print("{0} exists! Delay is: {1} minutes".format(morningTrip['trip_id'], delay))

#    for i in response.json():
#        if (i['id']=="UP-NW_UNW619_V1_B"):
#            print "UP-NW_UNW619_V1_B exists!"
#        print "id: {0}".format(i['id'])

#    print "Trip Updates:"
#    print(response.json()[1]['id'])

ProgramMain()