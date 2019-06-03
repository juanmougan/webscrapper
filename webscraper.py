from bs4 import BeautifulSoup
import requests
import sys
import re
import jsons

class UrlScraper:
	def parseArguments(self):
		if len(sys.argv) < 9:
			print ("Format: <program> <URL> <search string> <additional 6 css classes>")
			exit(1)
		self.base_url = str(sys.argv[1])
		self.search_string = str(sys.argv[2])
		self.holder = str(sys.argv[3])
		self.address_holder = str(sys.argv[4])
		self.link_holder = str(sys.argv[5])
		self.price_holder = str(sys.argv[6])
		self.rent_holder = str(sys.argv[7])
		self.expenses_holder = str(sys.argv[8])
		return (self.base_url + "/" + self.search_string)

class PriceInformation:
	def __init__(self, item, holder, rent_class, expenses_class):
		price_information = item.find('div', attrs={"class": holder})
		rent_str = price_information.find('p', attrs={"class": rent_class}).text.strip()
		self.rent = re.sub("[^0-9]", "", rent_str)
		expenses_unparsed = price_information.find('p', attrs={"class": expenses_class})
		print ("Type of expenses_unparsed: " + type(expenses_unparsed).__name__)
		if expenses_unparsed is not None:
			expenses_str = expenses_unparsed.text.strip()
			self.expenses = re.sub("[^0-9]", "", expenses_str)
		else:
			self.expenses = None
	# def serialize(self):
	# 	return {
	# 		rent: int(self.rent), 
	# 		expenses: int(self.expenses)
	# 	}
	# def __str__(self):
	# 	return "rent: {0}\texpenses: {1}".format(self.rent, self.expenses)
	# def __repr__(self):
	# 	return self.__str__()

class Article:
	def __init__(self, address, link, prices):
		self.address = address
		self.link = link
		self.prices = prices

scraper = UrlScraper()
url = scraper.parseArguments()
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

all_articles = []
for item in content.findAll('div', attrs={"class": scraper.holder}):
	address = item.find('h2', attrs={"class": scraper.address_holder}).text.strip()
	link = scraper.base_url + item.find('a', attrs={"class": scraper.link_holder}).get('href')
	prices = PriceInformation(item, scraper.price_holder, scraper.rent_holder, scraper.expenses_holder)

	article = Article(address, link, prices)
	all_articles.append(article)
	print (article)
	print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

print (jsons.dumps(all_articles))
