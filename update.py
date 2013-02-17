#!/usr/bin/python
import urllib2
import json
import logging
import sys
from BeautifulSoup import BeautifulSoup

ABOUT_PAGE = "https://github.com/about/team"

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)

def get_employees():
    '''
    Parse the about page since this isn't exposed via the api :(
    '''
    hubbers = []

    try:
        req = urllib2.Request(ABOUT_PAGE)
        raw_data = urllib2.urlopen(req).read()
    except urllib2.HTTPError:
        logging.exception("Could not get about page")
        return False

    soup = BeautifulSoup(raw_data)
    employees = soup.find('div', attrs={'class': 'employees'})
    for employee in employees.findAll('div', attrs={'class': 'employee_container'}):
        hubbers.append(employee.find('a')['href'].split('/')[-1])

    return hubbers

if __name__ == "__main__":
    employees = get_employees()
    with open('hubbers.js', 'w') as fh:
        fh.write(json.dumps(employees))
        fh.close()

