import sys
import time
import nltk
from nltk import word_tokenize
from urllib import request
import re
from os import path
from urllib import parse
from _custom import *


def search_wiki(title):
	title = re.sub(" ", "+", title)
	url = "https://en.wikipedia.org/w/index.php?sort=relevance&search=song+"+title
	
	try:
		response = request.urlopen(url)
	except:
		print(f"Failed. Trying again in 5 seconds ({url})")
		time.sleep(5)
		try:
			response = request.urlopen(url)
		except:
			print("Failed again. Skipping.")
			return False

	raw = response.read().decode('utf8')
	raw = raw[raw.index("<div class=\'mw-search-result-heading\'>")+38:]
	raw = raw[raw.index('<a href="')+9:]
	
	#raw = raw[raw.index('mw-search-result')+16:]
	raw = raw[:raw.index('"')]
	
	return "https://en.wikipedia.org"+raw
  

def scrape_wiki(url):
	try:
		response = request.urlopen(url)
	except:
		print(f"Failed. Trying again in 5 seconds ({url})")
		time.sleep(5)
		try:
			response = request.urlopen(url)
		except:
			print("Failed again. Skipping.")
			return False    
	
	raw = response.read().decode('utf8')
	try:
		raw = raw[raw.index('<table class="infobox vevent')+28:]
		year = raw[raw.index('>Released</th>')+14:]
		year = year[:year.index('</td>')]
		year = int(year[-4:])
		raw = raw[raw.index('>Genre</a>')+10:]
		genre = raw[:raw.index('</tr>')]
		genre = re.sub("[\[\<].*?[\>\]]", "", genre).strip()
		genre = re.sub("\n", ", ", genre)
		return year, genre
	except:
		print("Could not find expected infor on url", url)
		return False