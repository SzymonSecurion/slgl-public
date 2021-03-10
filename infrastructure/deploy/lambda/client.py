import requests
import urllib
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

url = "https://45o35kkpi7.execute-api.eu-west-1.amazonaws.com/Prod/"
user = "admin"
private_key = None

def post(id, type, extensions = {}):
    print(url)
    data = {
        "@id": id,
        "@type": type
    }
    for k, v in extensions.items():
        data[k] = v
    request = requests.post(url, json=data, auth=(user, private_key))
    if request.status_code == 409:
        print('Already exists')
    elif request.status_code != 200:
        print('Adding failed: {} status_code: {}'.format(request.json(),
                                                         request.status_code))
    else:
        print('Adding succeed: {}'.format(request.json(),
                                          request.status_code))
    return request

def link(link, type, value):
    print(url)
    verify_domain_request = {
        "@link": link,
        "@type": type,
        "value": value
    }
    request = requests.post(url, json=verify_domain_request, auth=(user, private_key))
    if request.status_code == 409:
        print('Already exists')
    elif request.status_code != 200:
        print('Adding failed: {} status_code: {}'.format(request.json(),
                                                         request.status_code))
    else:
        print('Adding succeed: {}'.format(request.json(),
                                          request.status_code))
    return request

def get(id):
    payload = {'show_state': 'show_fail_on_unauthorized', 'id': urllib.parse.unquote(id)}
    request = requests.get(url, params=payload, auth=(user, private_key))
    print(request.url)
    if request.status_code != 200:
        print('Getting failed: {} status_code: {}'.format(request.json(),
                                                          request.status_code))
    else:
        print('Getting succeed: {}'.format(request.json(),
                                           request.status_code))
    return request