#!/usr/bin/env python
import json
import os
import pprint
from twitter import OAuth, TwitterStream
import socket
import sys

oauth = OAuth(
    os.getenv('TWITTER_TOKEN'), os.getenv('TWITTER_TOKEN_SECRET'),
    os.getenv('TWITTER_CONSUMER_KEY'), os.getenv('TWITTER_CONSUMER_SECRET')
)

track = ['%s' % json.loads(row)['name'].encode(
    'utf8').replace(' ', '+') for row in sys.stdin]
print >>sys.stderr, ', '.join(track)

i = 0
twitter = TwitterStream(auth=oauth)
while True:
    print 'Start streaming tweets... %s' % (','.join(track))
    try:
        for tweet in twitter.statuses.filter(track=','.join(track)):
            print json.dumps(tweet)
            i = i + 1
            if i % 100 == 0 or i < 10:
                print >>sys.stderr, i, tweet[
                    'text'] if 'text' in tweet else '(empty tweet)'
    except socket.error:
        print >>sys.stderr, 'Socket error.'
print '...done streaming tweets.'
