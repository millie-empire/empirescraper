## Empire Scraper 0.0.1

The Empire Scraper will scrape all inputted empire webpages and output a list of external sites.

**Getting Started**

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

>Clone the repository from GitHub. Open up terminal and navigate to where you saved the repository. Then types the command: 
>
>```
>pip install -r requirements.txt
>```
>
>If you run into any issues, refer to the document below for alternative installation commands:
>https://doc.scrapy.org/en/latest/intro/install.html

**Running the Program**

Open up terminal and navigate to the first Empire_scraper within the downloaded repository. Then type the following code to run the Empire Scraper program:

```
scrapy crawl empire
```

Once the program has finished running, open the items.csv file. It should have two columns, link (list of external links) and link_from (origin of external links).

**Built With**

Scrapy - Python package used for scraping
