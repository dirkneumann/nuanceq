# -*-# coding: utf-8 -*-
import codecs
import json
import os
import pprint
import urllib
import urllib2
import sys


def query(typename, imagetype):

    out = sys.stdout

    emotion_names = ['happy', 'sad', 'surprised', 'angry', 'fearful', 'disgusted',
                     'rage', 'vigilance', 'ecstasy', 'admiration', 'terror', 'amazement', 'grief', 'loathing',
                     'anger', 'anticipation', 'joy', 'trust', 'fear', 'surprise', 'sadness', 'disgust', 'anger',
                     'annoyance', 'interest', 'serenity', 'acceptance', 'apprehension', 'distraction', 'thoughtful', 'boredom',
                     'aggressiveness', 'optimism', 'love', 'submission', 'awe', 'disapproval', 'remorse', 'contempt',
                     'hate']

    api_key = os.getenv('FREEBASE_KEY').strip()
    service_url = 'https://www.googleapis.com/freebase/v1/search'
    topic_id = '/celebrities/celebrity'  # '/m/0d6lp'
    params = {
        'key': api_key,
        'id': None,
        'name': None,
        'cursor': 0,
        'limit': 10,
        'type': typename,
        '/people/person/date_of_birth': None,
        'date_of_birth': None,
        '/common/topic/image': [{}],
    }

    cursor = 0
    while True:
        params['cursor'] = cursor
        url = service_url + '?' + urllib.urlencode(params)
        data = json.loads(urllib.urlopen(url).read())
        cursor += params['limit']

        if 'result' not in data:
            print >>sys.stderr, 'ERROR Freebase'
            print >>sys.stderr, data
            continue

        for datum in data['result']:

            if 'id' not in datum:
                datum['id'] = datum['mid']
            service_url2 = 'https://www.googleapis.com/freebase/v1/topic%s' % datum[
                'id']
            params2 = {
                'key': api_key,
                # '/common/topic/image,/people/person/date_of_birth',
                'filter': 'allproperties',
            }
            url = service_url2 + '?' + urllib.urlencode(params2)
            data2 = json.loads(urllib.urlopen(url).read())

            if 'id' not in data2:
                print >>sys.stderr, 'ERROR'
                continue
            # pprint.pprint(data2)
            try:
                print >>sys.stderr, data2['property'][
                    '/people/person/date_of_birth']['values'][0]['value']
            except KeyError:
                pass

            def bing_search(query, search_type='Image'):
                key = os.getenv('BING_API_KEY')
                query = urllib.quote(query)  # .encode('utf8'))
                #query = query.encode('utf8')
                print >>sys.stderr, query
                # create credential for authentication
                user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
                credentials = (':%s' % key).encode('base64')[:-1]
                auth = 'Basic %s' % credentials
                url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/' + \
                    search_type + '?Query=%27' + \
                    query + '%27&$top=5&$format=json'
                request = urllib2.Request(url)
                request.add_header('Authorization', auth)
                request.add_header('User-Agent', user_agent)
                request_opener = urllib2.build_opener()
                response = request_opener.open(request)
                response_data = response.read()
                json_result = json.loads(response_data)
                result_list = json_result['d']['results']
                # print result_list
                return result_list[0]['MediaUrl']

            print >>sys.stderr, datum['name']
            for keyword in [imagetype, ] + emotion_names:
                try:
                    image_url = bing_search(
                        u'%s %s %s' % (unicode(datum['name']), imagetype, keyword))
                    image = urllib.urlopen(unicode(image_url)).read()
                    filename = u'./static/images/%s.png' % (
                        '%s - %s' % (unicode(datum['name']), keyword))
                    print >>sys.stderr, filename
                    open(filename, 'w').write(image)
                except:
                    print >>sys.stderr, u'ERROR fetching image: %s' % unicode(
                        datum['name'])
                    import traceback
                    print >>sys.stderr, traceback.format_exc()

            for k, v in datum.iteritems():
                if k not in data2:
                    data2[k] = v
            x = json.dumps(data2)
            print >>out, x

if __name__ == '__main__':
    typename = sys.argv[1]
    imagetype = sys.argv[2]
    crawl(typename, imagetype)
