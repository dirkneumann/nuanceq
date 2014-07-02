#!/usr/bin/env python
from flask import *
import glob
import os
import urllib

app = Flask(__name__, static_folder='static', static_url_path='')

people = ['il-sung.png', 'obama.png', 'schwarzenegger.png']

cache = {}


@app.route('/loaderio-73acea61608a7544cc04f39a593f4833.txt')
def loader_io():
    return 'loaderio-73acea61608a7544cc04f39a593f4833'


@app.route('/data.json')
def data_json():
    emotion = request.args.get('emotion')
    if emotion in cache:
        return Response(cache[emotion])

    data = []
    for row in open('celebrities.json'):
        datum = json.loads(row)
        datum['image'] = '/static/images/%s.png' % urllib.quote(datum['name'])
        data.append(datum)

    cache[emotion] = json.dumps(data)

    return Response(json.dumps(data), mimetype='text')


@app.route('/')
def index():
    # redis.delete('search')
    #search = request.args.get('search')
    # if search:
    #    for w in search.split():
    #        redis.sadd('search', w)

    source = request.args.get('source', 'celebrity')
    emotion = request.args.get('emotion', 'happy')
    return render_template('analytics.html', emotion=emotion, source=source)
    # return render_template('index.html', emotion=emotion, source=source)


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/howitworks')
def howitworks():
    return render_template('howitworks.html')

app.run(host='0.0.0.0', port=int(
    os.getenv('PORT', '5000')), debug=True, threaded=True)
