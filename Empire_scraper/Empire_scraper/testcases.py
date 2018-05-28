import unittest
from Empire_scraper.spiders import MySpider
from responses import fake_response_from_file


class ScraperTest(unittest.TestCase):
	def setup(self):
		self.spider = MySpider.DirectorySpider()

		#allows access to google sheet
		credentials= googleapiclient._auth.with_scopes(googleapiclient._auth.default_credentials(), scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
		client = gspread.authorize(credentials)

		#reads in the google sheet
		sheet = client.open("Empire Scraper Output")
    	output_sheet = sheet.worksheet("Output")
    	
    	#takes in the first column of output (external links)
    	self.output_elink = []
    	for line in output_sheet.col_values(1):
        	self.output_elink.append(domain.strip())

        #takes in the second column of output (internal links)
        self.output_ilink = []
    	for line in output_sheet.col_values(2):
       		self.output_ilink.append(domain.strip())

        #importing allowed domains
        sheet = client.open("Empire Scraper Input")
    	alwd_domains_sheet = sheet.worksheet("AllowedDomains")
    	self.allowed_domains = []
    	for domain in alwd_domains_sheet.col_values(1):
        	self.allowed_domains.append(domain.strip())

        #importing the restricted domains
        restr_domains_sheet = sheet.worksheet("RestrictedDomains")
    	self.restricted_domains = []
    	for domain in restr_domains_sheet.col_values(1):
        	self.restricted_domains.append(domain.strip())

    #checks if external links contain the allowed domains
	def _test_external(self):
		for link in self.output_elink:
			for domain in self.allowed_domains:
				self.assertNotIn(domain, link)

	#check if the internal links contain the allowed domains
	def _test_internal(self):
		for link in self.output_ilink:
			for domain in self.allowed_domains:
				self.assertIn(domain, link)

	#check if the external links contain the restricted domains 
	def _test_restricted(self):
		for link in self.output_elink:
			for domain in self.restricted_domains:
				self.assertNotIn(domain, link)

	#check if the external links contain certain extensions
	def _test_redirect(self):
		for link in self.output_elink:
			self.assertTrue('.ly' not in link and '.am' not in link and 'redirect' not in link)

	#check if the scraper is able to get all the external links
	def _scraper_test(self):
		process = Crawler Process({
			'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
		})
		process.crawl(MySpider)
		process.start()



	#runs all the unit tests
	def test_all(self):
		self._test_external()
		self._test_internal()
		self._test_restricted()
		self._test_redirect()



