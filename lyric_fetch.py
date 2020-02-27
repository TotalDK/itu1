import sys
import time
import nltk
from urllib import request, parse
import re
from os import path
from _custom import *
from nltk import word_tokenize
from nltk.stem import PorterStemmer
import html

if path.isfile("failed_urls.txt"):
	with open("failed_urls.txt") as skipf:
		skip_url = set([line.strip() for line in skipf])
else:
	skip_url = set()

def search_wiki(title, artists, soundtrack = False):
	songtype = "soundtrack" if soundtrack else "song"
	print(f"Searching Wikipedia for {songtype} '{title}' by '{artists}' (this will most likely take some time).")
	title = re.sub(" ", "+", title)
	artists = re.sub(" ", "+", artists)
	url = "\thttps://en.wikipedia.org/w/index.php?sort=relevance&search=song+"+title+"+"+artists
	if soundtrack:
		url = url+"+soundtrack"
	print(url)
	
	try:
		response = request.urlopen(url)
	except:
		print(f"\tFailed Wiki search.")
		time.sleep(1)
		try:
			response = request.urlopen(url)
		except:
			print("\t\tFailed Wiki search again. Skipping.")
			return [False]

	raw = response.read().decode('utf8')

	try:
		raw = raw[raw.index("<div class=\'mw-search-result-heading\'>")+38:]
		raw = raw[raw.index('<a href="')+9:]
		result1 = raw[:raw.index('"')]
		try:
			raw = raw[raw.index("<div class=\'mw-search-result-heading\'>")+38:]
			raw = raw[raw.index('<a href="')+9:]
			result2 = raw[:raw.index('"')]
		except:
			print("Found only 1 search result.")
			return ["https://en.wikipedia.org"+result1]
	except:
		print("Found no search results. (url)")
		return [False]
	
	return ["https://en.wikipedia.org"+result1, "https://en.wikipedia.org"+result2]
  

def scrape_wiki(url):
	print(f"\tScraping Wikipedia page for year and genre:", url)
	try:
		response = request.urlopen(url)
	except:
		print(f"\t\tFailed URL open. Trying again in 5 seconds ({url})")
		time.sleep(5)
		try:
			response = request.urlopen(url)
		except:
			print("\t\t\tFailed URL open again. Skipping.")
			return False    
	
	raw = response.read().decode('utf8')
	try:
		raw = raw[raw.index('<table class="infobox vevent')+28:]
	except:
		print("\t\tCould not find '<table class=\"infobox vevent' in HTML string.")
		return False
	try:
		year = raw[raw.index('>Released</th>')+14:]
	except:
		print("\t\tCould not find ''>Released</th>'' in HTML string.")
		return False
	try:
		year = year[re.search(r"\d\d\d\d", year).start():]
		year = year[:4]
	except:
		print(f"Could not find proper release year. ({year})")
		return False
	try:
		raw = raw[raw.index('>Genre</a>')+10:]
		genre = raw[:raw.index('</tr>')]
		genre = re.sub("[\[\<].*?[\>\]]", "", genre).strip()
		genre = re.sub("\n", ", ", genre)
	except:
		print("\t\tCould not find ''>Genre</th>'' in HTML string.")
		return False
	
	return year, genre

def generatesong(disney, gender, url):
	#url = "https://www.azlyrics.com/lyrics/wizkhalifa/youngwildfree.html" #Example URL
	print("\nFetching lyrics from",url)

	try:
		response = request.urlopen(url)
	except:
		print(f"Failed. Trying again in {delay+5} seconds ({url})")
		time.sleep(delay+5)
		try:
			response = request.urlopen(url)
		except:
			print("Failed again. Skipping.")
			return None #None means url request denied
	#print("Fetched. Decoding ...")

	raw = response.read().decode('utf8')

	#print("Decoded. Stripping ...")
	if "www.azlyrics.com" in url:
		raw = raw[raw.index('<div class="lyricsh">')+30:]
		artists = raw[:raw.index(" Lyrics")]
		raw = raw[raw.index('<b>')+4:]
		title = raw[:raw.index('"</b>')]
		
		try:
			artists += ", " + raw[raw.index('<span class="feat">(with ')+25:raw.index(')<')]
		except:
			pass

		try:
			feat = raw[raw.index('(feat. ')+7:]
			feat = feat[:feat.index(')<')]
			artists += ", " + feat
		except:
			pass

		raw = raw[raw.index('<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->')+135:]
		raw = raw[:raw.index('\n</div>')]
	elif "www.lyrics.com" in url:
		raw = raw[raw.index('<h1 id="lyric-title-text" class="lyric-title">')+46:]
		title = raw[:raw.index('</h1>')]
		raw = raw[raw.index('<h3 class="lyric-artist"><a href=')+33:]
		raw = raw[raw.index('>')+1:]
		artists = raw[:raw.index('</a>')]
		while '<a href=' in raw[:50]:
			raw = raw[raw.index('<a href=')+9:]
			raw = raw[raw.index('>')+1:]
			artists += ", "+raw[:raw.index('</a>')]
		raw = raw[raw.index('<pre id="lyric-body-text"')+25:]
		raw = raw[raw.index('>')+1:]
		raw = raw[:raw.index('</pre>')]
	else:
		raise Exception("Unexpected lyric source: "+url+"\n"+raw)
	
	raw = re.sub("[\[\<].*?[\>\]]", "", raw).strip()
	artists = html.unescape(artists).strip()
	title = re.sub("[\[\<].*?[\>\]]", "", title).strip()
	title = html.unescape(title).strip()
	lyrics = html.unescape(raw).strip() #Already removed <>[] in raw.

	for search_result in search_wiki(title, artists):
		if search_result is False:
			continue
		year_genre = scrape_wiki(search_result)
		if year_genre is False:
			print(f"\t\tWiki scrape failed. ({search_result})")
		else:
			break
	else:
		for search_result in search_wiki(title, artists, True):
			if search_result is False:
				continue
			year_genre = scrape_wiki(search_result)
			if year_genre is False:
				print(f"\t\tWiki scrape failed. ({search_result})")
			else:
				break
		else:
			for search_result in search_wiki(title, "", True):
				if search_result is False:
					continue
				year_genre = scrape_wiki(search_result)
				if year_genre is False:
					print(f"\t\tWiki scrape failed. ({search_result})")
				else:
					break
			else:
				return False

	year, genre = year_genre
	
	genre = html.unescape(genre).strip()
	genre = re.sub("[\[\<].*?[\>\]]", "", genre).strip()

	return Song(title, year, genre, artists, gender, disney, lyrics)



if __name__ == "__main__":
	subdir = 'song_data'
	if not path.isdir(subdir):
		quit(f"This script needs the urls.txt file and folder named '{subdir}'.\nTo make sure you are creating the files in the right place, please create this folder yourself and run the script again.")
	
	print(f"Creating files in '{subdir}'.")
	print("\nIf you read this message, you have most likely not given the script a standard input.\n(You're probably looking to do 'python lyric_fetch.py < urls.txt')\n")
	overwrite = bool(int(input().strip()[-1]))
	delay = int(input().strip().split(" ")[-1])
	assert delay >= 0
	
	print(f"Overwrite is set to {overwrite}.")
	print("Pausing",delay,("second" if delay == 1 else "seconds"),"after each request.\n")

	here = path.dirname(path.realpath(__file__))
	for line in sys.stdin:
		line = line.strip()
		if line == '':
			continue
		
		disney, gender, url = line.strip().split(" ")
		
		filename = generatefilename(url)
		filepath = path.join(here, subdir, filename)
		if not overwrite:
			if path.isfile(filepath):
				print("\n"+filename, "already exists.")
				continue
			elif url in skip_url:
				print("\n"+filename, "failed last time. Skipping because Overwrite is set to False.")
				continue

		song = generatesong(disney, gender, url)
		if song is None:
			print(f"!!! Failed to generate song {filename} (HTML request failed - Possibly categorized as D-Dos attack) !!!")
			continue
		elif song is False:
			print(f"!!! Failed to generate song {filename} !!!")
			if path.isfile("failed_urls.txt"):
				with open("failed_urls.txt","a") as f2:
					f2.write(url+"\n")
			continue
		else:
			song.generatefile(filename, filepath)

		time.sleep(delay)