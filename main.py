from scrapy import cmdline
cmdline.execute("scrapy crawl restaurants -o quotes.json".split())
