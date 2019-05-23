from bs4 import BeautifulSoup
import requests
import sys

def parseArguments():
	if len(sys.argv) < 2:
		print ("Format: <program> URL")
		exit(1)
	return str(sys.argv[1])

url = parseArguments()
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

print (content)
