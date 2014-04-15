import requests
import json
import subprocess
import time
ACCESS_TOKEN = "CAADbJ2R6rpEBAKUP0NUVO5TrSQWk6B1pth9wxRQRZArTcvYvTAFHvw1AFh02qSAN8HZBGtVauDvQZAg61BpGzC3zcvYAkZAxOlyKsY4evM8t5LQ0ZAoYMfJpDSLMZBy4Qig9cP5JYeqQeLvMnhZAzgW4cccnZBr84KPMjrvaBOgPO90Gs0SkNYg1EIMdXnQDnQoZD"
friends_online = set()
friends_online_old = set() 
counter = 0

def get_friends_online():
    '''Returns friends who are online'''
    query = ("SELECT uid, name FROM user WHERE online_presence IN ('active', 'idle') AND uid IN (SELECT uid2 FROM friend WHERE uid1 = me())")

    payload = {'q' : query, 'access_token' : ACCESS_TOKEN }
    r = requests.get('https://graph.facebook.com/fql', params=payload)
    result = json.loads(r.text)
    for name in result['data']:
	    friends_online.add(name['name'])
    return friends_online

while 1:
    if counter % 30 == 0:
        friends_online_old = []
    if len(get_friends_online()) > 0:
        for friend in friends_online:
	        if not friend in friends_online_old:
	            message = "%s is online" % friend
	            subprocess.Popen(['notify-send', message])
	            friends_online_old.append(friend)
    time.sleep(60)
    counter += 1
