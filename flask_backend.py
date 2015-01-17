# PennApps

from flask import Flask, jsonify, render_template, request
import csv
import json
import requests

app = Flask(__name__)


@app.route('/')
def home():
    '''This is what you will see if you go to http://127.0.0.1:5000'''
    return 'Hello world.'


@app.route('/nutrition_facts', methods=['POST'])
def schedule():
    PM_Test_APIKey = 'ddc432d3-6900-44b0-84bf-58f3c16ef803'
    FE_APIKey = 'n54k3jg9cpkwzvaam4vavc7c'

    params = {'uid': 'user1', 'devid':'device1',
               'appide': 'heartmates', 'f':'json',
               'api_key': FE_APIKey}
    # data = {'api_key': 'n54k3jg9cpkwzvaam4vavc7c'}
    url_create = 'http://api.foodessentials.com/createsession'
    # set up session
    resp = requests.get(url_create, params=params)
    sid = resp.json()['session_id']

    # set profile
    

    # get profile
    url_profile = 'http://api.foodessentials.com/getprofile'
    params={'sid': sid,'f':'json','api_key': FE_APIKey}
    sid

    #resp = requests.post(url, data=data, headers=headers)







    schedule_courses = json.loads(request.form.get('foods'))
    food_items = json.loads(request.form.get(''))


    schedule = {
        'Monday':    [],
        'Tuesday':   [],
        'Wednesday': [],
        'Thursday':  [],
        'Friday': []
    }
    days = {'M': 'Monday', 'T': 'Tuesday', 'W': 'Wednesday',
            'R': 'Thursday', 'F': 'Friday'}
    course_matches = [get_courses(course['dept'], course[
        'code'], course['section'])[0] for course in schedule_courses]

    # I tried to do a dictionary comprehension for this, it ended up being
    # too difficult so I left it like this.
    for course in course_matches:
        for l in course['days']:
            schedule[days[l]].append('{}: {}'.format(course['name'].rstrip(
                ' '), course['times'].lstrip('MTWRF ').rstrip(' TBA')))

    return jsonify({days[day]: sorted(schedule[days[
        day]]) for day in days if schedule[days[day]] != []})


def main():
    import doctest
    options = (doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    print "Running doctests..."
    doctest.testmod(optionflags=options)


if __name__ == '__main__':
    import sys
    flag = sys.argv[1]
    if flag == 'doctests':
        main()
    elif flag == 'app':
        app.run(debug=True)
