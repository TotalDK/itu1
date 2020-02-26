import sys
import time
import nltk
from nltk import word_tokenize, FreqDist
from urllib import request
import re
from os import path
from urllib import parse
from _custom import *
import random
import pickle



if __name__ == "__main__":
	in_subdir = 'song_data'
	if not path.isfile("urls.txt") or not path.isfile("vector_config.txt") or not path.isdir(in_subdir):
		quit(f"This script needs the urls.txt file, vector_config.txt and the folder folders named '{in_subdir}' (input folder).\nTo make sure you are creating the files in the right place, please create these folders yourself and run the script again.")
	print(f"Converting song files from '{in_subdir}' and outputting featuresets in 'featuresets.pickle'.")
	print("\nIf nothing seems to be happening, you have most likely not given the script a standard input.\n(You're probably looking to do 'python song_data_to_vector_converter.py < urls.txt')\n")
	overwrite = bool(int(input().strip()[-1]))
	input() #Delay ignored.
	
	print(f"Overwrite is set to {overwrite}.")
	print("Not making requests, so ignoring Pause argument.\n")

	here = path.dirname(path.realpath(__file__))
	songs = []
	for line in sys.stdin:
		line = line.strip()
		if line == '':
			continue
		
		url = line.strip().split(" ")[2]
		
		in_filename = generatefilename(url)
		in_filepath = path.join(here, in_subdir, in_filename)
		if not overwrite and path.isfile("model.pickle"):
			print("'model.pickle' already exists.")
			continue
		song = readsong(in_filepath, in_filename, False, False, False) #Booleans are print optionals - first is for errors, second is for standard prints (success print)
		
		if song is not False:
			songs.append(song)

	with open("vector_config.txt") as config:
		_, max_years, max_genres, max_artists, max_tokens = (line.strip().split()[-1] for line in config)
	max_years, max_genres, max_artists, max_tokens = map(int, (max_years, max_genres, max_artists, max_tokens))

	most_popular_years = Song.most_popular('years', max_years)
	most_popular_genres = Song.most_popular('genres', max_genres)
	most_popular_artists = Song.most_popular('artists', max_artists)
	most_popular_tokens = Song.most_popular('tokens', max_tokens)
	assert most_popular_years and most_popular_genres and most_popular_artists and most_popular_tokens ##Assert all are not False
	#print(len(most_popular_years), len(most_popular_genres), len(most_popular_artists), len(most_popular_tokens))


	
	named_featuresets = []
	for song in songs:
		named_featuresets.append( song.vectorize(most_popular_years, most_popular_genres, most_popular_artists, most_popular_tokens) ) #(*years, *genres, *artists, *gender, *tokens), disney)
	
	random.seed(0)
	random.shuffle(named_featuresets)

	titleset, featuresets = [], []

	for title, featureset in named_featuresets:
		titleset.append(title)
		featuresets.append(featureset)
	
	with open("titleset.pickle","wb") as titleset_f:
		pickle.dump(titleset, titleset_f)
		print("titleset.pickle created.")
	
	with open("featuresets.pickle","wb") as featuresets_f:
		pickle.dump(featuresets, featuresets_f)
		print("featuresets.pickle created.")