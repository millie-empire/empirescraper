import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import Rule, BaseSpider
from Empire_scraper.items import EmpireScraperItem


import os #needed to allow deletion of files

#checks if items.csv file already exists 
def delete_file():
        #name of file containing the list of links
        myfile="/Users/citsbv/dev/empiresrcaper/empirescraper/Empire_scraper/items.csv"
    
        if os.path.isfile(myfile): #if file exists, delete it
            os.remove(myfile)
    
        else: #if file not found then show an error     
            print("Error: %s file not found" % myfile)

class MySpider(BaseSpider):
    name = "empire"
    
    #calls the method to check is items.csv exists (find where the file is 
    #created and move it there)
    delete_file()

    #only goes within the internal sites 
    #(finds external sites on the internal site)
    allowed_domains = ["empire.ca","empirelife.ca","empirelifeinvestments.ca"]

    #top-level URL
    start_urls = ["https://www.empire.ca/", "https://lifeandmoneymatters.empire.ca/", "https://plus.fastandfull.ca/"]

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
            
            # Check whether the domain of the URL of the link is allowed; so whether it is in one of the allowed domains
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



