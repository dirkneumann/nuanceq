# from word2vec import Word2Vec
import dateutil.parser
from gzip import GzipFile
import simplejson as json
import numpy as np
import text_nltk
from gzip import GzipFile
import pprint
from redis import Redis
import scipy.stats
import spark
import sys
import text_nltk


def redis():
    try:
        return redis.redis
    except AttributeError:
        redis.redis = Redis()
        return redis.redis


def mean_headline(x):
    if 'headline' not in x or 'main' not in x['headline'] or not x['headline']['main']:
        return None
    if 'lead_paragraph' not in x or not x['lead_paragraph']:
        return None
    words = text_nltk.lemma_tokenize(x['headline']['main'])
    if len(words) < 5:
        return None
    words += text_nltk.lemma_tokenize(x['lead_paragraph'])
    return np.nanmean([text_nltk.vectors(w) for w in words], axis=0)


def max_emotion(x):
    return sorted(x.iteritems(), key=lambda x: -x[1])[0][0]


def f_skip(f):
    def _f(x):
        fx = f(x)
        return [fx] if fx != None else []
    return _f


def add_(f):
    def _f(x):
        return (f(x), x)
    return _f


def _add(f):
    def _f(x):
        return (x, f(x))
    return _f


def add_skip(f):
    def _f(x):
        fk = f(x)
        return [(fk, x)] if fk != None else []
    return _f


def fk_(f):
    def _f(x):
        return (f(x[0]), x[1])
    return _f


def _fv(f):
    def _f(x):
        return (x[0], f(x[1]))
    return _f


def fk_skip(f):
    def _f(x):
        fk = f(x[0])
        return [(fk, x[0])] if fk != None else []
    return _f


def _fv_skip(f):
    def _f(x):
        fv = f(x[1])
        return [(x[0], fv)] if fv != None else []
    return _f


def skip_(f):
    def _f(x):
        fx = f(x)
        return [fx] if fx != None else []
    return _


def fk_skip(f):
    def _f(x):
        fk = f(x[0])
        return [(fk, x[1])] if fk != None else []
    return _f


def swap(x):
    return (x[1], x[0])


def fk(f):
    def _f(x):
        return f(x[0])
    return _f


def fv(f):
    def _f(x):
        return f(x[1])
    return _f


def k(x):
    return x[0]


def v(x):
    return x[1]


def dict_kv(x, k, v):
    x[k] = v
    return x


def divide(x):
    return x / x[0]

'''
prepend key - k_(f)
apply f to key  - fk_(f)
apply f to value - _fv(f)
drop key, v - k v
swap key, value - swap
lambda x: x[k] if k in x else None - nk_ _nv nx
(lambda x: x[k] if k in x else None)
'''

if False:
    test = sc.parallelize([
        '{"query": "John Doe", "pub_date": "today", "headline": {"main": "John is pleased today"}}',
        '{}',
        '{"query": "John Biggs", "pub_date": "today", "headline": {"main": "John is delighted today"}}'
    ]).flatMap(flat_json)

    assert test.count() == 3, "count != 3"
    assert test.take(1)[0]['query'] == "John Doe", "query not parsed"
    emotions = test.flatMap(f_skip(mean_headline)).map(
        empathy).map(max_emotion).collect()
    print emotions
    assert emotions[0] == 'happy', 'John Doe is not pleased: %s' % emotions[0]
    assert emotions[
        1] == 'happy', 'John Doe is not delighted: %s' % emotions[1]
    happiness = test.flatMap(f_skip(mean_headline)).map(
        empathy).map(lambda x: x['happy']).collect()
    print happiness
    assert happiness[0] >= happiness[
        1], 'pleased < delighted: %f %f' % happiness
    '''
    print test \
        .flatMap(k_skip(lambda x: x['query'] if 'query' in x else None))   \
        .flatMap(_fv_skip(mean_headline))  \
        .map(_fv(empathy))                 \
        .map(_fv(lambda x: x['happy']))    \
        .collect() #map(k_(empathy)).map(k_(max_emotion)).collect()
    '''
    articles = test.flatMap(
        add_skip(lambda x: (x['query'], x['pub_date']) if 'query' in x else None))
    scores   = articles   \
        .flatMap(_fv_skip(mean_headline))         \
        .map(_fv(lambda x: np.dot(x, text_nltk.vectors('happy'))))
    join     = articles   \
        .join(scores)     \
        .map(fv(lambda x: dict_kv(x[0], 'score', x[1]))) \
        .map(add_(lambda x: x['score'])).sortByKey(True).map(v).collect()
    assert join[0][
        'query'] == 'John Biggs', 'John Biggs is not the least happy after join.'

    print >>sys.stderr, 'TEST OK'

'''
    .join(test2)                           \
    .map(v(lambda x: dict_kv(x[1], 'score', x[0])))                 \
    .map(lambda x: dict_kv(x, 'image', '/static/images/%s.png' % x['query'])) \
'''

# define the text data RDD and the dictionary RDD
#data = sc.textFile("s3n://insight-data-oregon/data/nyt2/", 20).map(json.loads)
#data = sc.textFile("file:///mnt/data/1403309348.json.gz").parallelize(40).map(json.loads)
#data = sc.parallelize(GzipFile('/mnt/data/1403309348.json.gz'), 10).map(json.loads)
#data = sc.textFile('s3n://insight-data-oregon/20140625_nyt.json.gz').repartition(10).flatMap(flat_json)
'''
data = {}

data['brand'] = sc.textFile('s3n://insight-data-oregon/20140627_business_brand_nyt.json.gz').repartition(39).flatMap(flat_json).cache()
data['celebrity'] = sc.textFile("file:///mnt/data/1403309348.json.gz").repartition(40).flatMap(flat_json).cache()
#data = sc.textFile('s3n://insight-data-oregon/business_brand_nyt2.json', 10).repartition(10).map(json.loads)
#data = data.sample(False, 0.1).cache()
print '\n\nPartitions: %i\n\n' % data['brand']._jrdd.splits().size()
print '\n\nPartitions: %i\n\n' % data['celebrity']._jrdd.splits().size()

article_index = {}
article_vector = {}
identity_vector = {}
for k in data:
    article_index[k]   = data[k].flatMap(add_skip(lambda x: (x['query'], x['pub_date'])))
    article_vector[k]  = article_index[k].flatMap(_fv_skip(mean_headline))
    identity_vector[k] = article_vector[k]          \
        .map(fk_(lambda x: x[0]))             \
        .reduceByKey(lambda a, b: a+b)        \
        .filter(lambda x: x[1][0] >= 3)       \
        .map(_fv(divide)).cache()
'''


def check_headline(x):
    # check full name
    tf_query = x['query'] in x['headline']['main']
    if 'seo' in x['headline']:
        tf_query = tf_query or x['query'] in x['headline']['seo']
    if 'print_headline' in x['headline']:
        tf_query = tf_query or x['query'] in x['headline']['print_headline']
    # check last name
    last_ind = x['query'].rfind(' ')
    if last_ind > 0:
        last_name = x['query'][(last_ind + 1):]
        tf_query = tf_query or last_name in x['headline']['main']
        if 'seo' in x['headline']:
            tf_query = tf_query or last_name in x['headline']['seo']
        if 'print_headline' in x['headline']:
            tf_query = tf_query or last_name in x['headline']['print_headline']
    return tf_query

# filter those who does not appear in the title
#data = data.filter(check_headline)
# print 'data count after headline filtering'
#dic = sc.textFile("s3n://insight-data-oregon/vectors_25d.txt.gz").map(lambda x: x.split(' ')).map(lambda x: (x[0], [1.0,]+map(float,x[1:])))


def x_text(x):
    return x['headline']['main'] if 'headline' in x and 'main' in x['headline']['main'] and x['headline']['main'] else None

# pick lead paragraph - tokenize and lammentize
'''
print data.take(1)
article_index  = data.flatMap(add_skip(lambda x: (x['query'], x['pub_date'])))
article_vector = article_index.flatMap(_fv_skip(mean_headline))
identity_score  = article_vector          \
    .map(fk_(lambda x: x[0]))             \
    .reduceByKey(lambda a, b: a+b)        \
    .map(_fv(divide))                     \
    .map(_fv(empathy))
'''

result_format = lambda x: {
    'name': x[1], 'score': x[0], 'image': '/static/images/%s.png' % x[1]}
#result_format = lambda x: {'name': x[1][0], 'score': x[0] if not np.isnan(x[0]) else 0, 'image': '/static/images/%s.png' % x[1][0], 'time': x[1][1]}

'''
emotion = 'happy'
text = json.dumps(article_vector.map(empathy).take(1)) #map(lambda x: (x[1][emotion], x[0])).filter(lambda x: not np.isnan(x[0])).sortByKey(False).map(result_format).take(36))
print text
sys.exit()
'''


def confusion(model=None):
    emotions = ['joy', 'sadness', 'disgust', 'anger', 'surprise', 'fear']
    data = spark.data('semeval', cores=16)   \
        .map(lambda x: spark.dict_kv(x,
                                     'emotion',
                                     text_nltk.empathy(
                                         text_nltk.mean_vector(
                                             x['text'], model=model),
                                         model=model
                                     )
                                     )).collect()
    sample = data[0]
    print >>sys.stderr, sample
    results = []
    for emotion in emotions:
        for prediction in sample['emotion'].keys():
            x = np.asarray([float(row[emotion]) for row in data])
            y = np.asarray([row['emotion'][prediction] for row in data])
            ind = np.where((np.isnan(x) + np.isnan(y)) == 0)
            z = (emotion, prediction, ) + scipy.stats.pearsonr(x[ind], y[ind])
            results.append(
                {'emotion': z[0], 'vector': z[1], 'r': z[2], 'p': z[3]})
    return results


def add_emotion(a, b):
    if 'n' not in a:
        a['n'] = 1
    if 'n' not in b:
        b['n'] = 1
    for k in a:
        a[k] = a[k] + (b[k] if k in b else 0)
    return a


def div_emotion(a):
    n = a['n'] if 'n' in a else 1
    for k in a:
        a[k] = a[k] / n
    return a


def all_identities(source, model=None):
    if not model:
        model = 'vectors_25d'
    return spark.data(source, cores=4)   \
        .map(lambda x: ((x['query'], '%s-01' % x['pub_date'][:7]), text_nltk.empathy(x['headline_main_%s' % model], model=model)))   \
        .reduceByKey(add_emotion).map(lambda x: {'query': x[0][0], 'pub_date': x[0][1], 'emotion': div_emotion(x[1])}).collect()


def top_articles(source, emotion):
    return article_vector[source]   \
        .map(_fv(lambda x: np.dot(text_nltk.vectors(emotion), x)))   \
        .map(fk_(lambda k: k[1]))      \
        .map(swap).sortByKey(False)    \
        .map(result_format).take(36)


def all_articles(source, model=None):
    if not model:
        model = 'vectors_25d'
    results = spark.data(source, cores=16).map(lambda x: dict_kv(
        x, 'emotion', text_nltk.empathy(x['headline_main_%s' % model], model=model)))
    return results.collect()


def submit_response(key, data):
    redis().set(key, json.dumps(data, ignore_nan=True))
    redis().publish('response', key)


def listen_redis():
    pubsub = redis().pubsub()
    pubsub.subscribe('command')
    for item in pubsub.listen():
        print item
        if item['type'] == 'message':
            params = redis().hgetall(item['data'])
            key = params['__key']
            del params['__key']
            print >>sys.stderr, 'KEY: %s' % key
            if key.endswith('all_articles.json'):
                submit_response(key, all_articles(params['source']))
                continue
            if 'all_identities.json' in key:
                submit_response(key, all_identities(
                    params['source'], model=params['model'] if 'model' in params else None))
                continue

            if key.endswith('confusion.json'):
                submit_response(
                    key, confusion(model=params['model'] if 'model' in params else None))
                continue
            if key.endswith('top.json'):
                submit_response(
                    key, top_json(params['source'], params['emotion'], params['identity']))
                continue

            print key
            print params
            #submit_response(key, params)

if __name__ == '__main__':
    listen_redis()
