import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import Rule, BaseSpider
from Empire_scraper.items import EmpireScraperItem
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from pathlib import Path


import os #needed to allow deletion of files

#checks if items.csv file already exists 
#os.remove("/Users/citmst/dev/empirescraper/Empire_scraper/Empire_scraper/items.csv")

my_file = Path("./items.csv")
if my_file.is_file():
   os.remove(my_file)

class MySpider(BaseSpider):
    name = "empire"

    #only goes within the internal sites 
    #(finds external sites on the internal site)
    #allowed_domains = ["empire.ca","empirelife.ca","empirelifeinvestments.ca"]

    with open('allowed_domains.txt') as f1:
            allowed_domains = []
            for url in f1:
                allowed_domains.append(url.strip())
            f1.close()

    #top-level URL
    #start_urls = ["https://www.empire.ca/", "https://lifeandmoneymatters.empire.ca/", "https://plus.fastandfull.ca/"]

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse"
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        with open('start_urls.txt') as fp:
                for line in fp:

        #for url in self.start_urls:
                    yield Request(line.strip(), callback=self.parse)
        fp.close()

    def parse(self, response):
        items = []     
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)                         
        for link in links:
            
            # Check whether the domain of the URL of the link is external; 
            # so checks that it is not in allowed_domains
            is_allowed = True
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = False
            # If it is an external link, create a new item and add it to the list of found items
            if is_allowed:
                item = EmpireScraperItem() 
                item['link_from'] = response.url
                item['link'] = link.url
                items.append(item)
        
        return items



