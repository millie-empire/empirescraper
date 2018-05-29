import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors import IGNORED_EXTENSIONS
from scrapy.spiders import Rule, Spider
from Empire_scraper.items import EmpireScraperItem
from scrapy.http import Request
from scrapy import signals
import googleapiclient._auth #needed to get API credentials
import gspread #needed to write to google spreadsheets
from pydispatch import dispatcher

#allows the code to access googlesheets 
credentials= googleapiclient._auth.with_scopes(googleapiclient._auth.default_credentials(), scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
client = gspread.authorize(credentials)
 

#definition of the spider (used to crawl and scrape webpages)
class MySpider(Spider):

    #name of project
    name = "empire"

    def __init__(self):
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    #imports the allowed domains (defines what an internal link contains) 
    #from the google spreadsheet 
    sheet = client.open("Empire Scraper Input")
    alwd_domains_sheet = sheet.worksheet("AllowedDomains")
    allowed_domains = []
    for domain in alwd_domains_sheet.col_values(1):
        allowed_domains.append(domain.strip())


    #imports restricted domains (defines what links to ignore)
    restr_domains_sheet = sheet.worksheet("RestrictedDomains")
    restricted_domains = []
    for domain in restr_domains_sheet.col_values(1):
        restricted_domains.append(domain.strip())


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
        #opens the google spreadsheet with the start_urls (urls to scrape first)
        sheet = client.open("Empire Scraper Input")
        start_sheet = sheet.worksheet("StartUrls")

        #scrapes each start_url
        for item in start_sheet.col_values(1):
            yield Request(item.strip(), callback=self.parse)

    items = []  
    i = 0
    internal_links = set()

    # Dictionary {'facebook.com': ['empire.ca'], 'twitter.com': ['empire.ca']}
    output = list()

    def parse(self, response):
             
        links = LinkExtractor(canonicalize=True, unique=True, deny_extensions=IGNORED_EXTENSIONS).extract_links(response)       
              
                          
        for link in links:
           
            # check if link contains an allowed domain 
            internal_link = False
            for allowed_domain in self.allowed_domains:
                if allowed_domain in link.url:
                    internal_link = True

            #checks if link contains a restricted domains
            is_allowed = True
            for restricted_domain in self.restricted_domains:
                if restricted_domain in link.url:
                    is_allowed = False


            if is_allowed:

                #checks if link has any of the following strings
                if ".ly" in link.url or ".am" in link.url or "redirect" in link.url:
                    yield scrapy.Request(link.url, callback=self.parse) 

                #external link added to dictionary if it is not already contained
                elif not internal_link:
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

                # adds internal link to the dictionary if it is not there
                elif link.url not in self.internal_links:
                    self.internal_links.add(link.url)
                    # recursively checks internal links that have not been checked
                    yield scrapy.Request(link.url, callback=self.parse)

            #self.i += 1
        

    # output to Google sheets before spider closes
    def spider_closed(self, spider):
        #opens the output spreadsheet
        sheet = client.open("Empire Scraper Output")
        output_sheet = sheet.worksheet("Output")
 
        #clears the data on the sheet
        output_sheet.clear()

        # prints titles of columns
        output_sheet.update_cell(1,1,'External Link')
        output_sheet.update_cell(1,2,'Found on this Page')

        #gets the range of the spreadsheet
        external_list = output_sheet.range('A2:A1000')
        internal_list = output_sheet.range('B2:B1000')

        index = 0

        for item in self.items:  
            # print external link
            external_list[index].value = item['link']
            for internal_link in item['link_from']:
                # print corresponding internal links for external link
                internal_list[index].value = internal_link
                index += 1

        #updates to Google sheet
        output_sheet.update_cells(external_list)
        output_sheet.update_cells(internal_list)



