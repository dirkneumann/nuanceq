Nuance/Q
====

Nuance/Q reads articles, and summarizes the meaning of the lead paragraph in semantic vector space.

For politicians and brands, it shows the predominant emotion over time.

    USAGE: nuance.py [cmd]
 
      source .env        # aws, bing, freebase, nyt keys
 
      nuance.py query /business/brand logo >/mnt/data/20140701_business_brand.json
      nuance.py query /celebrities/celebrity portait >/mnt/data/20140701_celebrities_celebrity.json
      nuance.py query /government/politician portait >/mnt/data/20140701_government_politician.json
 
      nuance.py crawl </mnt/data/20140701_business_brand.json >/mnt/data/20140701_business_brand_nyt.json
      nuance.py crawl </mnt/data/20140701_celebrities_celebrity.json >/mnt/data/20140701_celebrities_celebrity_nyt.json
      nuance.py crawl </mnt/data/20140701_government_politician.json >/mnt/data/20140701_government_politician_nyt.json
 
      hadoop fs -cp /mnt/data/20140701_government_politician_nyt.json /
 
      spark-submit ./nuanceq.py ingest celebrities_celebrity.json.gz hdfs:///celebrities_celebrity_vectors_50d
      spark-submit ./nuanceq.py backend
 
      nuance.py api     # api.nuanceq.com
      nuance.py front   # nuanceq.com

© 2014 Dirk Neumann
