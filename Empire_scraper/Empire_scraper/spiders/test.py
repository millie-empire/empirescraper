from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from Empire_scraper.items import EmpireScraperItem

import os #needed to allow deletion of files


class MySpider(BaseSpider):
    name = "empire"
    
    #only goes within the internal sites 
    #(finds external sites on the internal site)
    allowed_domains = ["craigslist.org"]

    #top-level URL
    start_urls = ["http://columbusga.craigslist.org/search/reo/"]

    #name of file containing the list of links
    myfile="/Users/citsbv/dev/empiresrcaper/empirescraper/Empire_scraper/Empire_scraper/items.csv"
    
    if os.path.isfile(myfile): #if file exists, delete it
        os.remove(myfile)
    
    else: #if file not found then show an error     
        print("Error: %s file not found" % myfile)

    def parse(self, response):
        titles = response.selector.xpath("//p")
        items = []
        for titles in titles:
            item = EmpireScraperItem()
            item["title"] = titles.select("a/text()").extract()
            item["link"] = titles.select("a/@href").extract()
            
            if ("/6584243056.html" not in str(item["link"])):
                items.append(item)
    
        return items
