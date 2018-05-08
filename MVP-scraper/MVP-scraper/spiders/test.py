from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from MVP-scraper.items import CraigslistSampleItem

class MySpider(BaseSpider):
    name = "craig"
    allowed_domains = ["craigslist.org"]
    start_urls = ["http://columbusga.craigslist.org/search/reo/"]

    def parse(self, response):
        titles = response.selector.xpath("//p")
        items = []
        for titles in titles:
            item = CraigslistSampleItem()
            item["title"] = titles.xpath("a/text()").extract()
            item["link"] = titles.xpath("a/@href").extract()
            items.append(item)
        return items
