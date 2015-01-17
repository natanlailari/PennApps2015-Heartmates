# PennApps

from flask import Flask, jsonify, request
import csv
import json

app = Flask(__name__)


@app.route('/')
def home():
    '''This is what you will see if you go to http://127.0.0.1:5000'''
    return 'Hello world.'


@app.route('/nutrition_facts', methods=['POST'])
def schedule():
    ''' A POST-only endpoint. Accept POST data of the form:
    {'foods': [ list of foods ]}
    format?

    Suppose the list of courses is:
    [{'dept': 'ACCT', 'code': '297', 'section': '402'},
     {'dept': 'MATH', 'code': '104', 'section': '226'},
     {'dept': 'CIS', 'code': '521', 'section': '001'}]

    Note that when sending this data, we need to JSON-encode it,
    i.e. turn the list into a string that can be sent over HTTP:
    req = requests.post(.., data={'courses': json.dumps(list_of_courses)})

    Then req.json() should equal:
    {
        u'Monday':    [u'Taxes And Bus Strategy: 12-1:30PM'],
        u'Tuesday':   [u'Fundamentals Of Ai: 10:30-12NOON'],
        u'Wednesday': [u'Calculus I: 9-10AM',
                       u'Taxes And Bus Strategy: 12-1:30PM']
        u'Thursday':  [u'Fundamentals Of Ai: 10:30-12NOON'],
    }

    Some notes:
    1. Remember that dictionaries are unordered data structures, so the order
    of keys does not matter.
    2. The class lists should be in alphabetical order of class name.
    3. If there is no class on a day, don't include a key for that day.
    '''
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
