from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from Empire_scraper.items import EmpireScraperItem
import os


class MySpider(BaseSpider):
    name = "empire"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://columbusga.craigslist.org/search/reo/"]

    myfile="/Users/citsbv/dev/empiresrcaper/empirescraper/Empire_scraper/Empire_scraper/items.csv"

    # if file exists, delete it
    if os.path.isfile(myfile):
        os.remove(myfile)
    else:    # show an error
        print("Error: %s file not found" % myfile)

    def parse(self, response):
        titles = response.selector.xpath("//p") 
        items = []                              
        for titles in titles:
            item = EmpireScraperItem()         
            item["title"] = titles.select("a/text()").extract()   # gets title
            item["link"] = titles.select("a/@href").extract()     # gets link
            
            if ("/6584243056.html" not in str(item["link"])):     # filters out internal sites
                items.append(item)
    
        return items
