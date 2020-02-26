import sys
import time
import nltk
from nltk import word_tokenize
from urllib import request
import re

class Song():
	tokenset = set()
	def __init__(self, title, year, artists, gender, disney, lyrics):
		self.title = title
		self.year = year
		self.artists = artists
		self.gender = gender
		self.lyrics = lyrics
		self.disney = disney
		self.tokens = word_tokenize(self.lyrics)
		self.tokencount = {token:self.tokens.count(token) for token in set(self.tokens)}
		print(self.title, "("+self.year+")", "-", self.artists, "("+self.gender+")", "-", ("(Disney song)" if self.disney else "(Not a Disney song)"))
		self.update_tokenset()

	def update_tokenset(self):
		Song.tokenset.update(self.tokens)

	def __str__(self):
		return "<Song '" + self.title + "' by '" + self.artists +"'>"


def generatesongs():
	#url = "https://www.azlyrics.com/lyrics/wizkhalifa/youngwildfree.html" #Example URL
	songlist = []
	for url in sys.stdin:
		if url == '':
			continue
		disney, gender, year, url = url.strip().split(" ")
		disney = int(disney)
		#print("Fetching lyrics from",url,"...")
		
		if "www.azlyrics.com" in url:
			print("AZLyrics url skipped due to fetch complications.")
			continue
		
		try:
			response = request.urlopen(url)
		except:
			print("Failed. Trying again. ("+url.strip()+")")
			time.sleep(5)
			try:
				response = request.urlopen(url)
			except:
				print("Failed again. Skipping.")
			continue
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
		artists = artists.replace('&amp;', '&').strip()
		title = title.replace('&amp;', '&').strip()
		lyrics = raw.replace('&amp;', '&').strip()

		songlist.append(Song(title, year, artists, gender, disney, lyrics))
	return songlist


songs = generatesongs()
print(len(Song.tokenset))