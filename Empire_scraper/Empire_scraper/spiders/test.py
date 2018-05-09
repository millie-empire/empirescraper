from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from Empire_scraper.items import EmpireScraperItem


class MySpider(BaseSpider):
    name = "empire"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://columbusga.craigslist.org/search/reo/"]

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
