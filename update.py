#!/usr/bin/python
import urllib2
import json
import logging
import sys
from urllib import quote
from BeautifulSoup import BeautifulSoup

ABOUT_PAGE = "https://github.com/about/team"
USER_API = "https://api.github.com/users/%s"
OPT_ARGS = "client_id=something&" \
    "client_secret=something"

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)


def get_hubbers():
    '''
    Parse the about page since this isn't exposed via the api :(
    Returns a list of usernames pulled from the href
    '''
    hubbers = []

    try:
        req = urllib2.Request('%s?%s' % (ABOUT_PAGE, OPT_ARGS))
        raw_data = urllib2.urlopen(req).read()
    except urllib2.HTTPError:
        logging.exception("Could not get about page")
        return False

    soup = BeautifulSoup(raw_data)
    employees = soup.find('div', attrs={'class': 'employees'})
    for employee in employees.findAll('div',
                                      attrs={'class': 'employee_container'}):
        hubbers.append(employee.find('a')['href'].split('/')[-1])

    return hubbers


def convert_location_to_latlng(location):
    '''
    Takes a location name and returns the lat/lng as a tuple
    '''
    loc = quote(location)
    try:
        req = urllib2.Request("http://maps.googleapis.com/maps/api/geocode/"
                              "json?address=%s&sensor=false" % loc)
        raw_data = urllib2.urlopen(req).read()
    except urllib2.HTTPError:
        logging.exception("Could not get location for %s" % loc)
        return False

    data = json.loads(raw_data)
    if len(data) > 0:
        lng = data['results'][0]['geometry']['location']['lng']
        lat = data['results'][0]['geometry']['location']['lat']
        return (lng, lat)


def get_user_profile(user):
    '''
    Takes a username and returns their profile (name/nick/avatar/location)
    '''
    user = quote(user)
    try:
        req = urllib2.Request('%s?%s' % (USER_API % user, OPT_ARGS))
        raw_data = urllib2.urlopen(req).read()
    except urllib2.HTTPError:
        logging.exception("Could not get profile for %s" % user)
    else:
        data = json.loads(raw_data)

        profile = {
            'username': user,
            'avatar': data['avatar_url'],
            'name': data['name'],
        }

        if 'location' in data.keys() and data['location']:
            loc = data['location'].encode('utf-8')
            (lng, lat) = convert_location_to_latlng(loc)
            profile['location_lat'] = lat
            profile['location_lng'] = lng

            return profile
    return False

if __name__ == "__main__":
    '''
    This logic should be in a function but oh well
    '''
    hubbers = {}

    for hubber in get_hubbers():
        profile = get_user_profile(hubber)
        if profile:
            hubbers[hubber] = profile

    with open('hubbers.js', 'w') as fh:
        fh.write(json.dumps(hubbers))
        fh.close()
