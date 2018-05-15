import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Spider
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

class MySpider(Spider):
    name = "empire"

    #only goes within the internal sites 
    #(finds external sites on the internal site)
    #allowed_domains = ["empire.ca","empirelife.ca","empirelifeinvestments.ca"]

    with open('allowed_domains.txt') as file:
            allowed_domains = []
            for url in file:
                allowed_domains.append(url.strip())
            file.close()

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
        with open('start_urls.txt') as file:
                for url in file:
                    yield Request(url.strip(), callback=self.parse)
        file.close()

    items = []  
    i = 0
    internal_links = set()
    def parse(self, response):
          
             
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)       
                        
                          
        for link in links:
                # Check whether the domain of the URL of the link is external; 
                # so checks that it is not in allowed_domains
            #if self.i < 50:
            is_allowed = True
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    is_allowed = False
                    # If it is an external link, create a new item and add it to the list of found items
            if is_allowed:
                recorded = False
                for i in self.items:
                    if link.url == i['link']:
                        recorded = True
                        i['link_from'].append(response.url)
                        break
                
                if not recorded:
                    item = EmpireScraperItem() 
                    item['link_from'] = []
                    item['link_from'].append(response.url)
                    item['link'] = link.url
                    self.items.append(item)
                    #if item['link'] not in self.items:
                        # with open('items.csv','a+') as f:
                        #     f.write("{}\n".format('\t'.join(str(item[field]) 
                        #         for field in fields)))
                        #     f.close()
                        #self.items.append(item)



            # internal link but not checked and is not a document
            elif link.url not in self.internal_links and "document" not in link.url:
                self.internal_links.add(link.url)
                # recursively checks internal links that have not been checked
                yield scrapy.Request(link.url, callback=self.parse)

            #self.i += 1

    fields = ["link", "link_from"]  
    with open('items.csv','a+') as f:
        for this in items:    
            f.write("{}\n".format('\t'.join(str(this[field]) 
                    for field in fields)))
    f.close()


        #print("hello", self.items)
        # fields = ["link", "link_from"] # define fields to use
        # with open('items.csv','a+') as f: # handle the source file
        #     # f.write("{}\n".format('\t'.join(str(field) 
        #     #     for field in fields))) # write header
        #     for url in self.items:
        #         f.write("{}\n".format('\t'.join(str(url[field]) 
        #             for field in fields))) # write items

        #return self.items



