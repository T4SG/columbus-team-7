from flask import Flask
import speechparser
import dataset
import os
import json
import StringIO
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

app = Flask(__name__)
db = dataset.connect("sqlite:///C:/users/jake/skydrive/projects/jpmc-cfg-cmh-15/cfgcmhdb.db")
table = db['user']

os.chdir("C:/users/jake/skydrive/projects/jpmc-cfg-cmh-15/")


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/parse/<user>/<speech>')
def parsealexa(user, speech):
    general_sentiment = speechparser.parsestring(speech)
    total_sentiment = speechparser.overall_sentiment(speech)
    grades = speechparser.get_grades_sentiment(speech)
    attendance = speechparser.get_attendance_sentiment(speech)
    participation = speechparser.get_participation_sentiment(speech)

    table.insert(dict(username=user, general_sentiment=general_sentiment, grades=grades, attendance=attendance,
                      participation=participation))

    return "ok"

@app.route('/get/<user>/data')
@crossdomain(origin='*')
def get_data(user):
    set = table.find(username=user)

    dataset.freeze(set, format='json', filename="export.json")
    with open("C:/users/jake/skydrive/projects/jpmc-cfg-cmh-15/export.json", 'r') as exportfile:
        toreturn = exportfile.read()
    os.remove("C:/users/jake/skydrive/projects/jpmc-cfg-cmh-15/export.json")
    return toreturn


if __name__ == '__main__':
    app.debug = True
    app.run()
