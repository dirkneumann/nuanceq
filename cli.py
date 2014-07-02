import back
import datetime
import freebase
import ingest
import json
import nyt
from pprint import pprint
import server
import spark
import sys
import text_nltk

if __name__ == '__main__':
    today = datetime.date.today()
    today_str = '%04i%02i%02i' % (today.year, today.month, today.day)
    if len(sys.argv) == 1:
        print 'USAGE: cli.py [cmd]'
        print ' '
        print '  source .env'
        print '  python cli.py query /business/brand logo >/mnt/data/%s_business_brand.json' % today_str
        print '  python cli.py query /celebrities/celebrity portait >/mnt/data/%s_celebrities_celebrity.json' % today_str
        print '  python cli.py query /government/politician portait >/mnt/data/%s_government_politician.json' % today_str
        print '  gzip /mnt/data/%s_celebritites_celebrity.json'
        print ' '
        print '  python cli.py crawl </mnt/data/%s_business_brand.json >/mnt/data/%s_business_brand_nyt.json' % ((today_str, ) * 2)
        print '  python cli.py crawl </mnt/data/%s_celebrities_celebrity.json >/mnt/data/%s_celebrities_celebrity_nyt.json' % ((today_str, ) * 2)
        print '  python cli.py crawl </mnt/data/%s_government_politician.json >/mnt/data/%s_government_politician_nyt.json' % ((today_str, ) * 2)
        print ' '
        print '  spark-submit cli.py ingest celebrities_celebrity.json.gz hdfs:///celebrities_celebrity_text8'
        print '  spark-submit cli.py back'
        print ' '
        print '  python cli.py server'
        print ' '
        sys.exit()
    if sys.argv[1] == 'back':
        back.listen_redis()
    if sys.argv[1] == 'crawl':
        nyt.crawl()
    if sys.argv[1] == 'emotions':
        print json.dumps(back.confusion(), indent=2)
        '''
        for row in back.all('hdfs:///1403223397_nyt_text8'):
            print json.dumps(row)
        '''
    if sys.argv[1] == 'ingest':
        ingest.nyt(sys.argv[2], sys.argv[3])
    if sys.argv[1] == 'server':
        server.serve()
    if sys.argv[1] == 'query':
        freebase.query(sys.argv[2], sys.argv[3])
