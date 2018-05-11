import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import Rule, BaseSpider
from Empire_scraper.items import EmpireScraperItem
from pathlib import Path
import os #needed to allow deletion of files

#checks if the items.csv file exists, if it does then it gets deleted
my_file = Path("/Users/citsbv/downloads/testcrawl/testcrawl/testing.csv")
if my_file.is_file():
   os.remove(my_file)

class MySpider(BaseSpider):
    name = "empire"
    
    #only goes within the internal sites 
    #(finds external sites on the internal site)
    allowed_domains = ["empire.ca","empirelife.ca","empirelifeinvestments.ca", "empirelife-prod.auth0.com", "empire.wistia.com"]

    #top-level URL
    start_urls = ["https://www.empire.ca/"]

    #the spider has one rule: extract all (unique and canonicalized) links, 
    #follow then and parse them using the parse_items method
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
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        items = []     
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)                         
        for link in links:
            
            # Check whether the domain of the URL of the link is allowed; 
            # so whether it is in one of the allowed domains
            is_allowed = True
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = False
            
            # If it is allowed, create a new item and add it to the list of found items
            if is_allowed:
                item = EmpireScraperItem() 
                item['link_from'] = response.url
                item['link'] = link.url
                items.append(item)
        
        return items
