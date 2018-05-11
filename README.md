#Empire Scraper 0.0.1

The Empire Scraper will scrape the homepage of empire.ca and output a list of external sites.

**Getting Started**
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

**Prerequisites**
To install Scrapy, open up terminal and type the command: 

```
pip install scrapy
```

If you run into any issues, refer to the document below for alternative installation commands:
https://doc.scrapy.org/en/latest/intro/install.html

**Running the Program**
Clone the repository from GitHub. Open up terminal and navigate to the first Empire_scraper folder you downloaded. Then type the following code to run the Empire Scraper program:

```
scrapy crawl empire
```

Once the program has finished running, open the items.csv file. It should have two columns, link (list of external links) and link_from (origin of external links), similar to the image below:


**Built With**
Scrapy - Python package used for scraping
