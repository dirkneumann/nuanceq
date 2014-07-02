Nuance/Q
====

Nuance/Q reads articles, and summarizes the meaning of the lead paragraph in semantic vector space.

For politicians and brands, it shows the predominant emotion over time.

    USAGE: cli.py [cmd]
 
      source .env
      python cli.py query /business/brand logo >/mnt/data/20140701_business_brand.json
      python cli.py query /celebrities/celebrity portait >/mnt/data/20140701_celebrities_celebrity.json
      python cli.py query /government/politician portait >/mnt/data/20140701_government_politician.json
      gzip /mnt/data/%s_celebritites_celebrity.json
 
      python cli.py crawl </mnt/data/20140701_business_brand.json >/mnt/data/20140701_business_brand_nyt.json
      python cli.py crawl </mnt/data/20140701_celebrities_celebrity.json >/mnt/data/20140701_celebrities_celebrity_nyt.json
      python cli.py crawl </mnt/data/20140701_government_politician.json >/mnt/data/20140701_government_politician_nyt.json
 
      spark-submit cli.py ingest celebrities_celebrity.json.gz hdfs:///celebrities_celebrity_text8
      spark-submit cli.py back
 
      python cli.py server

© 2014 Dirk Neumann
