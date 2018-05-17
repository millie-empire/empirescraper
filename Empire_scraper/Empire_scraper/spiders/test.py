import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, Spider
from Empire_scraper.items import EmpireScraperItem
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from pathlib import Path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os #needed to allow deletion of files

#allows the code to access googlesheets 
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
 
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Test sheet").sheet1

#clears the data on the sheet
cell_list = sheet.range('A1:Z1000')
for cell in cell_list:
    cell.value = ' '
sheet.update_cells(cell_list)

#definition of the spider
class MySpider(Spider):
    name = "empire"

    #Method that scrapes the webpages if their url
    #contain the domains from the allowed domains google sheet
    allowed_domains = []
    sheet = client.open("Empire scraper input")
    ad_sheet = sheet.worksheet("Sheet2")
    #sheet = client.open("Empire scraper input").sheet2
    x = [item for item in ad_sheet.col_values(1) if item]
    for item in x:
        allowed_domains.append(item.strip())

    #parameters for how the scraper should work
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
        #opens the google spreadsheet with the start_urls
        sheet = client.open("Empire scraper input")
        start_sheet = sheet.worksheet("Sheet1")

        #scrapes each start_url
        x = [item for item in start_sheet.col_values(1) if item]
        for item in x:
            yield Request(item.strip(), callback=self.parse)

    items = []  
    i = 1
    j = 1
    internal_links = set()

    def parse(self, response):
          
        #downloads the pages to be scraped     
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)       
        fields = ["link", "link_from"]                  
                          
        for link in links:
            # Check whether the domain of the URL of the link is external; 
            # so checks that it is not in allowed_domains
            if self.i < 20:
                is_allowed = True
                for allowed_domain in self.allowed_domains:
                    if allowed_domain in link.url:
                        is_allowed = False
                # If it is an external link, create a new item and add it to the list of found items
                if is_allowed:
                    item = EmpireScraperItem() 
                    item['link_from'] = response.url
                    item['link'] = link.url
                    
                    if item['link'] not in self.items:
                        # opens the output google sheet and writes
                        #the external link and the webpage it came from
                        sheet = client.open("Test sheet").sheet1
                        sheet.update_cell(1,1, 'External link')
                        sheet.update_cell(1,2, 'Found on this page')
                        sheet.update_cell(self.j+1,1, item['link'])
                        sheet.update_cell(self.j+1,2, item['link_from'])
                        self.j+=1

                        self.items.append(item)


                # internal link but not checked and is not a document
                elif link.url not in self.internal_links and "document" not in link.url:
                    self.internal_links.add(link.url)
                    # recursively checks internal links that have not been checked
                    yield scrapy.Request(link.url, callback=self.parse)
           
        self.i += 1


