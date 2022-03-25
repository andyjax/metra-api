import json
import sys
import requests
import urllib3

def ProgramMain():
    urllib3.disable_warnings()

    with open('credential.json') as creds:
        apiCred=json.load(creds)
    
    authKey = apiCred['authorization']

    payload = ""
    headers = {
        'Authorization': authKey,
        'cache-control': "no-cache"
    }

    url = "https://gtfsapi.metrarail.com/gtfs/alerts"
    response = requests.request("GET", url, data=payload, headers=headers)
#    response_json = response.json()

#    print("stopping")
    printed = 0
    for i in response.json():
        if (i['alert']['informed_entity'][0]['route_id']=="UP-NW"):
            print('\033[1m' + i['alert']['header_text']['translation'][0]['text'] + '\033[0m')
            print("\t" + i['alert']['description_text']['translation'][0]['text'])
            printed = 1
    
    if (printed == 0):
        print('\033[93m' + "No alerts for UP-NW line!" + '\033[0m')

ProgramMain()