from urllib import request, parse
from nltk.corpus import stopwords
import re
from os import path, stat
import time
from nltk import word_tokenize
from nltk.stem import PorterStemmer

ps = PorterStemmer()


class Song():
	yeardict = dict()
	genredict = dict()
	artistdict = dict()
	tokendict = dict()
	disneycount = 0
	nondisneycount = 0
	def __init__(self, title, year, genres, artists, gender, disney, lyrics):
		self.title = title
		self.year = year
		self.genres = genres.split(", ")
		self.artists = artists.split(", ")
		self.gender = gender
		self.disney = int(disney)
		self.lyrics = " ".join(lyrics.split())
		assert type(lyrics) == str
		self.tokens = word_tokenize(lyrics)
		assert type(self.tokens) == list
		stop_words = set(stopwords.words("english"))
		stop_words.update([',','.','(',')',"'",'"','[',']','===','!','?',"''",'``','...'])
		self.tokens = [ps.stem(token.lower()) for token in self.tokens]
		self.tokens = [token for token in self.tokens if not token in stop_words]
		self.update_yeardict(self.year)
		self.update_genredict(self.genres)
		self.update_artistdict(self.artists)
		self.update_tokendict(self.tokens)
		self.update_count(self.disney)

	@classmethod
	def update_yeardict(cls, year):
		if year in cls.yeardict:
			cls.yeardict[year] += 1
		else:
			cls.yeardict[year] = 1

	@classmethod
	def update_genredict(cls, genres):
		for genre in genres:
			if genre in cls.genredict:
				cls.genredict[genre] += 1
			else:
				cls.genredict[genre] = 1

	@classmethod
	def update_artistdict(cls, artists):
		for artist in artists:
			if artist in cls.artistdict:
				cls.artistdict[artist] += 1
			else:
				cls.artistdict[artist] = 1

	@classmethod
	def update_tokendict(cls, tokens):
		for token in set(tokens):
			if token in cls.tokendict:
				cls.tokendict[token] += tokens.count(token)
			else:
				cls.tokendict[token] = tokens.count(token)

	@classmethod
	def update_count(cls, disney):
		if disney:
			cls.disneycount += 1
		else:
			cls.nondisneycount += 1

	def __str__(self):
		return "<Song: "+self.title+" ("+self.year+")"+" ("+", ".join(self.genres)+")"+" - "+", ".join(self.artists)+" ("+self.gender+")"+" - "+("(" if self.disney else "(Not a ")+"Disney song)>"

	def generatefile(self, filename, filepath):
		try:
			with open(filepath, 'w') as f:
				f.write("\n".join([self.title,self.year, ", ".join(self.genres), ", ".join(self.artists), self.gender, str(self.disney), self.lyrics]))
				print(filename, "created.\n")
		except IOError:
			print("Wrong path provided.")

	def vectorize(self, top_years, top_genres, top_artists, top_tokens):
		#(*years, *genres, *artists, *gender, *tokens), disney)
		years_subdict = {"year:"+year:(year == self.year) for year in top_years}
		genres_subdict = {"genre:"+genre:(genre in self.genres) for genre in top_genres}
		artists_subdict = {"artist:"+artist:(artist in self.artists) for artist in top_artists}
		gender_subdict = {"gender":(self.gender == "M")}
		tokens_subdict = {"token:"+token:(token in self.tokens) for token in top_tokens}
		combined_subdict = {**years_subdict, **genres_subdict, **artists_subdict, **gender_subdict, **tokens_subdict}
		return (self.title, (combined_subdict, ("Disney" if self.disney else "Not Disney")))

	@classmethod
	def most_popular(cls, feature):
		if feature == 'years':
			featurelist = list(cls.yeardict.items())
		elif feature == 'genres':
			featurelist = list(cls.genredict.items())
		elif feature == 'artists':
			featurelist = list(cls.artistdict.items())
		elif feature == 'tokens':
			featurelist = list(cls.tokendict.items())
		else:
			print("Feature '{feature}' not found.")
			return False
		featurelist.sort(key = lambda x: x[1], reverse=True)
		return [featuretuple[0] for featuretuple in featurelist[:int(.2*len(featurelist))]]

class TestSong(Song): #Copy of Song class. Used to distinguish test songs from non-test songs.
	yeardict = dict()
	genredict = dict()
	artistdict = dict()
	tokendict = dict()
	disneycount = 0
	nondisneycount = 0

class Song0(Song): #Copy of Song class. Used to distinguish test songs from non-test songs.
	yeardict = dict()
	genredict = dict()
	artistdict = dict()
	tokendict = dict()
	disneycount = 0
	nondisneycount = 0

class DevSong(Song): #Copy of Song class. Used to distinguish test songs from non-test songs.
	yeardict = dict()
	genredict = dict()
	artistdict = dict()
	tokendict = dict()
	disneycount = 0
	nondisneycount = 0



def readsong(filepath, filename = None, pr_nf = False, pr_e = False, pr = False):
	if filename is None:
		filename = filepath

	if not path.isfile(filepath):
		if pr_nf:
			print(filename, "doesn't exist.")
		return False
	
	if stat(filepath).st_size == 0:
		if pr_e:
			print(filename, "found but empty. Skipping.")
		return False

	with open(filepath, "r") as f:
		try:
			title, year, genre, artists, gender, disney, lyrics = (line.strip() for line in f)
			try:
				year = str(int(year))
			except:
				if pr_e:
					print(filename, f"found but year was in wrong format. Skipping. ({year})")
				return False
		except:
			if pr_e:
				print(filename, "found but unsuccessfully loaded. Skipping.")
			return False
		#year = int(year)
		if pr:
			print(filename, "sucessfully loaded.")
		return title, year, genre, artists, gender, disney, lyrics

def generatefilename(url):
	filename = parse.unquote(url)
	filename = filename[filename.rindex("/")+1:] #rindex() is reverse index().
	filename = filename.replace('.html', '')
	filename = re.sub("[^A-Za-z]","",filename)+".txt" #If needed, \W is pythonic regex for "all characters that are not numbers, letters or underscore.
	return filename