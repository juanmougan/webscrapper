from bs4 import BeautifulSoup
import requests
import sys

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
	def __init__(self, holder, rent_class, expenses_class):
		price_information = content.find('div', attrs={"class": holder})
		self.rent = price_information.find('p', attrs={"class": rent_class}).text.strip()
		self.expenses = price_information.find('p', attrs={"class": expenses_class}).text.strip()

scraper = UrlScraper()
url = scraper.parseArguments()
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

for item in content.findAll('div', attrs={"class": scraper.holder}):
	print ("Address: ")
	address = content.find('h2', attrs={"class": scraper.address_holder}).text.strip()
	print (address)
	print ("Link: ")
	link = scraper.base_url + content.find('a', attrs={"class": scraper.link_holder}).get('href')
	print (link)
	prices = PriceInformation(scraper.price_holder, scraper.rent_holder, scraper.expenses_holder)
	print ("Rent: ")
	print (prices.rent)
	print ("Expenses: ")
	print (prices.expenses)
	print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
