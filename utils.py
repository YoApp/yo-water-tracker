# -*- coding: utf-8 -*-
import requests


def get_remote_addr(request):
    address = request.headers.get('X-Forwarded-For', request.remote_addr)
    if address is not None:
        address = address.encode('utf-8')
        address = address.split(',')[0]
    else:
        address = request.remote_addr

    return address


def get_location_data(ip):
    geoip_server = 'http://ec2-54-152-137-106.compute-1.amazonaws.com:8080/json'
    if not (ip and geoip_server):
        return

    url = '%s/%s' % (geoip_server, ip)
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print 'Error fetching location: ' + sys.exc_info()