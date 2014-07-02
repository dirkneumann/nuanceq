#!/usr/bin/env python
# -*- coding: utf-8 -*-

import api
import backend
import datetime
import ingest.freebase
import ingest.nyt
import json
from pprint import pprint
import spark
import sys
import text_nltk

if __name__ == '__main__':
    today = datetime.date.today()
    today_str = '%04i%02i%02i' % (today.year, today.month, today.day)
    if len(sys.argv) == 1:
        print 'USAGE: ./nuance.py [cmd]'
        print ' '
        print '  source .env        # aws, bing, freebase, nyt keys'
        print ' '
        print '  nuance.py query /business/brand logo >/mnt/data/%s_business_brand.json' % today_str
        print '  nuance.py query /celebrities/celebrity portait >/mnt/data/%s_celebrities_celebrity.json' % today_str
        print '  nuance.py query /government/politician portait >/mnt/data/%s_government_politician.json' % today_str
        print ' '
        print '  nuance.py crawl </mnt/data/%s_business_brand.json >/mnt/data/%s_business_brand_nyt.json' % ((today_str, ) * 2)
        print '  nuance.py crawl </mnt/data/%s_celebrities_celebrity.json >/mnt/data/%s_celebrities_celebrity_nyt.json' % ((today_str, ) * 2)
        print '  nuance.py crawl </mnt/data/%s_government_politician.json >/mnt/data/%s_government_politician_nyt.json' % ((today_str, ) * 2)
        print ' '
        print '  hadoop fs -cp /mnt/data/%s_government_politician_nyt.json /' % (today_str, )
        print ' '
        print '  spark-submit ./nuanceq.py ingest celebrities_celebrity.json.gz hdfs:///celebrities_celebrity_vectors_50d'
        print '  spark-submit ./nuanceq.py backend'
        print ' '
        print '  nuance.py api     # api.nuanceq.com'
        print '  nuance.py front   # nuanceq.com'
        print ' '
        sys.exit()
    
    if sys.argv[1] == 'api':
        api.serve()
    if sys.argv[1] == 'backend':
        backend.listen_redis()
    if sys.argv[1] == 'crawl':
        ingest.nyt.crawl()
    if sys.argv[1] == 'emotions':
        print json.dumps(backend.confusion(), indent=2)
    if sys.argv[1] == 'ingest':
        ingest.nyt(sys.argv[2], sys.argv[3])
    if sys.argv[1] == 'query':
        ingest.freebase.query(sys.argv[2], sys.argv[3])
