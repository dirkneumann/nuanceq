import back
from flask import *
from flask.ext.compress import Compress
import os
from redis import Redis
import urllib
import sys


def redis():
    try:
        return redis.redis
    except AttributeError:
        redis.redis = Redis()
        return redis.redis


def json_api(f):
    def _f():
        text = f()
        response = Response(text, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    return _f


def report_error(f):
    def wrapper():
        try:
            return f()
        except:
            etype, value, tb = sys.exc_info()
            import traceback
            return '<br>\n'.join(traceback.format_exception(etype, value, tb))
    return wrapper


def pubsub():
    try:
        return pubsub.pubsub
    except AttributeError:
        pubsub.pubsub = redis().pubsub()
        pubsub.pubsub.subscribe('response')
        return pubsub.pubsub


def redis_call(key, params={}):
    __key = '%s/%s' % (key, urllib.urlencode(params))
    text = redis().get(__key)
    if text != None:
        return text

    params['__key'] = __key
    key2 = 'command/%s' % __key
    print key2
    redis().hmset(key2, params)
    redis().publish('command', key2)

    for item in pubsub().listen():
        print 'item:', item
        if item['type'] == 'message':
            data = redis().get(item['data'])
            return data


def serve():
    compress = Compress()
    app = Flask(__name__, static_folder='static')
    compress.init_app(app)

    @app.route('/top_identities.json', methods=['GET', 'POST'])
    @json_api
    def top_identities():
        source = request.args.get('source', 'celebrity')
        emotion = request.args.get('emotion', 'happy')
        key = '%s x %s' % (source, emotion)
        text = redis().hget('top_identities.json', key)
        if not text:
            text = json.dumps(back.top_identities(source, emotion))
            redis().hset('top_identities.json', key, text)
        return text

    @app.route('/top_articles.json', methods=['GET', 'POST'])
    def top_articles():
        source = request.args.get('source', 'celebrity')
        emotion = request.args.get('emotion', 'happy')
        key = '%s x %s' % (source, emotion)
        text = redis().hget('top_articles.json', key)
        if not text:
            text = json.dumps(back.top_articles(source, emotion), indent=4)
            redis().hset('top_articles.json', key, text)
        return text

    @report_error
    @json_api
    @app.route('/all_articles.json', methods=['GET', 'POST'])
    def all_articles():
        source = request.args.get(
            'source', '20140629_government_politician_nyt')
        model = request.args.get('model', 'vectors_50d')
        text = redis().get('all_articles.json')
        if not text:
            text = redis_call(
                'all_articles.json', {'source': 'hdfs:///%s' % source, 'model': model})
            redis().set('all_articles.json', text)
        return text

    #@report_error
    #@json_api
    @app.route('/all_identities.json', methods=['GET', 'POST'])
    def all_identities():
        source = request.args.get(
            'source', '20140629_government_politician_nyt')
        model = request.args.get('model', 'vectors_50d')
        text = redis_call(
            'all_identities.json', {'source': 'hdfs:///%s' % source, 'model': model})
        response = Response(text, mimetype='application/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    @json_api
    @report_error
    @app.route('/confusion.json', methods=['GET', 'POST'])
    def confusion():
        key = 'json'
        text = redis().hget('confusion.json', key)
        if not text:
            text = redis_call(
                'confusion.json', {'source': 'semeval', 'model': 'twitter_vectors_20d'})
            redis().hset('confusion.json', key, text)
        return text

    # running the api
    app.run(host='0.0.0.0', port=int(
        os.getenv('PORT', '80')), debug=True, threaded=True)

if __name__ == '__main__':
    serve()
