from bs4 import BeautifulSoup
from firestore_client import FirestoreClient
import requests
import sys
import re
import jsons

OUTPUT_FILE = "estate.json"
COLLECTION = u'articles'

class UrlScraper:
	def parseArguments(self):
		if len(sys.argv) < 9:
			print ("Format: <program> <URL> <search string> <additional 6 css classes> <credential files>")
			exit(1)
		self.base_url = str(sys.argv[1])
		self.search_string = str(sys.argv[2])
		self.holder = str(sys.argv[3])
		self.address_holder = str(sys.argv[4])
		self.link_holder = str(sys.argv[5])
		self.price_holder = str(sys.argv[6])
		self.rent_holder = str(sys.argv[7])
		self.expenses_holder = str(sys.argv[8])
		self.creds = str(sys.argv[9])
		return (self.base_url + "/" + self.search_string)

class PriceInformation:
	def __init__(self, item, holder, rent_class, expenses_class):
		price_information = item.find('div', attrs={"class": holder})
		rent_str = price_information.find('p', attrs={"class": rent_class}).text.strip()
		self.rent = int(re.sub("[^0-9]", "", rent_str))
		expenses_unparsed = price_information.find('p', attrs={"class": expenses_class})
		if expenses_unparsed is not None:
			expenses_str = expenses_unparsed.text.strip()
			self.expenses = int(re.sub("[^0-9]", "", expenses_str))
		else:
			self.expenses = None

class Article:
	def __init__(self, address, link, rent, expenses):
		self.address = address
		self.link = link
		self.rent = rent
		self.expenses = expenses

	def __eq__(self, other):
		if not isinstance(other, Article):
		# Don't attempt to compare against unrelated types
			return NotImplemented
		# I don't care about prices for comparison
		return self.address == other.address and self.link == other.link

	def __hash__(self):
		return hash((self.address, self.link))

	def __str__(self):
		return "Address: " + self.address + "\tLink: " + self.link + "\tRent: " + str(self.rent) + "\tExpenses: " + str(self.expenses)

	def __add__(self, other):
		return str(self) + other

	def __radd__(self, other):
		return other + str(self)

def prettyPrintToJsonFile(articles):
	output_file = open(OUTPUT_FILE, "w")
	output_file.write(jsons.dumps(all_articles, indent=4, sort_keys=True))
	output_file.close()

def mapDictToArticle(a):
	rent = None
	expenses = None
	try:
		rent = a["prices"]["rent"]
		expenses = a["prices"]["expenses"]
	except:
		a["prices"] = None
	print("CREATED AN ARTICLE")
	return Article(a["address"], a["link"], rent, expenses)

def uploadToFirestore(creds, articles):
	print("Uploading to Firestore")
	client = FirestoreClient(creds, COLLECTION)
	saved_articles_dict = client.fetch_all_from_collection()
	print("\n\n\n\n\nsaved_articles_dict size: " + str(len(saved_articles_dict)))
	print(saved_articles_dict)
	saved_articles = map(mapDictToArticle, saved_articles_dict)
	print("\n\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n\n")
	#print("saved_articles size: " + str(len(saved_articles)))
	saved_articles_set = set()
	for a in saved_articles:
		#print("Saved article: " + a)
		saved_articles_set.add(a)
	print("saved_articles_set size: " + str(len(saved_articles_set)))
	
	articles_set = set(articles)
	#for a in articles_set:
	#	print("Saved article: " + a)	
	print("\n\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n\n")
	print("articles_set size: " + str(len(articles_set)))
	
	#saved_articles_set = set()
	#for sa in saved_articles:
	#	saved_articles_set.add(sa)
	
	to_be_saved = articles_set - saved_articles_set
	print("to_be_saved size: " + str(len(to_be_saved)))
	print("\n\n\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n\n\n")
	for article in to_be_saved:
		print("Will save Article: " + article)
		client.store_in_collection(article)

scraper = UrlScraper()
url = scraper.parseArguments()
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

all_articles = []
for item in content.findAll('div', attrs={"class": scraper.holder}):
	address = item.find('h2', attrs={"class": scraper.address_holder}).text.strip()
	link = scraper.base_url + item.find('a', attrs={"class": scraper.link_holder}).get('href')
	try:
		prices = PriceInformation(item, scraper.price_holder, scraper.rent_holder, scraper.expenses_holder)
	except AttributeError:
		continue	# I don't want an Article without prices!
	article = Article(address, link, prices.rent, prices.expenses)
	all_articles.append(article)
	print(f"Adding {address}	{link}	{prices.rent}	{prices.expenses}")
	print ("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

print ("Will print results to file: " + OUTPUT_FILE)
prettyPrintToJsonFile(all_articles)

uploadToFirestore(scraper.creds, all_articles)
