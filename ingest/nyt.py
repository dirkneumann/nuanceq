#!/usr/bin/env python
import json
from nytimesarticle import articleAPI
import os
import sys
import time

n = 0
t = time.time()

api = articleAPI(os.getenv('NYT_API_KEY'))


def invert(name):
    parts = name.split()
    return '%s, %s' % (parts[-1], ' '.join(parts[:-1]))


def crawl():
    for row in sys.stdin:  # open('celebrities.json'):
        try:
            entry = json.loads(row)
        except:
            print >>sys.stderr, 'ERROR parsing input file'
            continue
        name = entry['name']

        print >>sys.stderr, name

        n = 0
        for i in range(0, 100):
            while (n / (time.time() - t)) >= 2:
                print >>sys.stderr, '.'
                time.sleep(1)
            try:
                articles = api.search(fq='persons:("%s") OR persons:("%s") OR organizations:("%s")' % (
                    name, invert(name), name), page=i, sort='newest')
                docs = articles['response']['docs']
                for doc in docs:
                    for k in entry:
                        if k not in doc:
                            doc[k] = entry[k]
                    doc["query"] = name
                    print json.dumps(doc)
                n += len(docs)
                print >>sys.stderr, n
                if len(docs) == 0:
                    break
            except:
                print >>sys.stderr, sys.exc_info()[0]
                print >>sys.stderr, 'ERROR'
                time.sleep(1)

if __name__ == '__main__':
    crawl()
