import unittest
import googleapiclient._auth
import gspread

#from scrapy.spiders import Spider


class ScraperTest(unittest.TestCase):
	def setUp(self):
		#self.spider = Spider.MySpider()

		#allows access to google sheet
		credentials= googleapiclient._auth.with_scopes(googleapiclient._auth.default_credentials(), scopes=['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive'])
		client = gspread.authorize(credentials)

		#reads in the google sheet
		sheet = client.open("Empire Scraper Output")
		output_sheet = sheet.worksheet("Output")
		output_expected = sheet.worksheet("Unittest")

		#takes in the first column of output (external links)
		self.output_elink = []
		for line in output_sheet.col_values(1):
			self.output_elink.append(line.strip())

		#takes in the second column of output (internal links)
		self.output_ilink = []
		for line in output_sheet.col_values(2):
			self.output_ilink.append(line.strip())

		internal_expected = 1
		self.expected = {}
		for line in output_expected.col_values(1):
			internal_link = output_expected.cell(internal_expected, 2)
			if line.strip():
				external_link = line.strip()
				self.expected[external_link] = [internal_link]
			else:
				self.expected[external_link].append(internal_link)
			internal_expected += 1

		internal_output = 1
		self.output = {}
		for line in output_sheet.col_values(1):
			internal_link = output_sheet.cell(internal_output, 2)
			if line.strip():
				external_link = line.strip()
				self.output[external_link] = [internal_link]
			else:
				self.output[external_link].append(internal_link)
			internal_output += 1

		#importing allowed domains
		sheet = client.open("Empire Scraper Input")
		alwd_domains_sheet = sheet.worksheet("AllowedDomains")
		self.allowed_domains = []
		for domain in alwd_domains_sheet.col_values(1):
			self.allowed_domains.append(domain.strip())

		restr_domains_sheet = sheet.worksheet("RestrictedDomains")
		self.restricted_domains = []
		for domain in restr_domains_sheet.col_values(1):
			self.restricted_domains.append(domain.strip())

    #checks if external links contain the allowed domains
	def test_external(self):
		for link in self.output_elink:
			for domain in self.allowed_domains:
				self.assertNotIn(domain, link)

	#check if the internal links contain the allowed domains
	def test_internal(self):
		for link in self.output_ilink:
			for domain in self.allowed_domains:
				self.assertIn(domain, link)

	#check if the external links contain the restricted domains 
	def test_restricted(self):
		for link in self.output_elink:
			for domain in self.restricted_domains:
				self.assertNotIn(domain, link)

	#check if the external links contain certain extensions
	def test_redirect(self):
		for link in self.output_elink:
			self.assertTrue('.ly' not in link and '.am' not in link and 'redirect' not in link)

	#check if the scraper is able to get all the external links
	def test_scrape_all(self):

		for ext in self.output:
			self.assertIn(ext,self.expected)
			
			for inter in self.output[ext]:
				self.assertIn(inter,self.expected[ext])
			
			int_count = count_internal(self.output[ext])
			exp_int_count = count_internal(self.expected[ext])
			assertTrue(int_count == exp_int_count)

		assertTrue(len(self.expected.keys()) == len(self.output.keys()))

	def count_internal(links):
		count = 0
		for link in links:
			count += 1

		return count
			

#runs all the unit tests
if __name__ == '__main__':
	unittest.main()



