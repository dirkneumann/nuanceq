import csv
import json
from StringIO import StringIO
import sys


def dict_kv(x, k, v):
    x[k] = v
    return x


def sc(cores=None, pyFiles=['back.py', 'cli.py', 'ingest.py', 'spark.py', 'text_nltk.py', 'spark.py', 'word2vec.py'], memo=None):
    if not cores:
        cores = 4
    try:
        return sc.sc
    except AttributeError:
        from pyspark import SparkConf, SparkContext
        print >>sys.stderr, "CORES: %i" % cores
        conf = SparkConf()
        conf.setAppName("Nuance/Q%s" % (" [%s]" % memo if memo else ""))
        conf.set("spark.executor.memory", "8g")
        conf.set("spark.cores.max", str(cores))
        conf.set("master.ui.port", "8082")
        conf.set("spark.ui.port", "4041")  # kicked in

        sc.sc = SparkContext(conf=conf, pyFiles=pyFiles)
        return sc.sc


def data(name, cores=None):
    try:
        d = data.data
    except AttributeError:
        data.data = {}
    if name not in data.data:
        if 'semeval' in name:
            import text_nltk
            data.data[name] = sc(cores=cores, memo=name)   \
                .textFile('s3n://insight-data-oregon/affectivetext_test.emotions.csv.gz')  \
                .repartition(39)                \
                .map(parse_csv_f())             \
                .cache()
        elif 'nyt' in name:
            data.data[name] = sc(cores=cores, memo=name)   \
                .textFile(name)                 \
                .repartition(39)                \
                .flatMap(flat_json)             \
                .cache()
        else:
            data.data[name] = sc(cores=cores, memo=name)   \
                .textFile(name)                 \
                .flatMap(flat_json)             \
                .cache()
    return data.data[name]


def flat_json(x):
    try:
        return [json.loads(x)]
    except:
        return []


def parse_csv_f(fieldnames=['id', 'anger', 'disgust', 'fear', 'joy', 'sadness', 'surprise', '_diff', '_id', 'text']):
    def _f(row):
        return csv.DictReader(StringIO(row), fieldnames=fieldnames).next()
    return _f
