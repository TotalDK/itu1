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
import math
import copy



if __name__ == "__main__":
	in_subdir = 'song_data'
	if not path.isfile("urls.txt")  or not path.isdir(in_subdir):
		quit(f"This script needs the urls.txt file and the folder folders named '{in_subdir}' (input folder).\nTo make sure you are creating the files in the right place, please create these folders yourself and run the script again.")
	print(f"Converting song files from '{in_subdir}' and outputting featuresets in 'featuresets.pickle'.")
	print("\nIf nothing seems to be happening, you have most likely not given the script a standard input.\n(You're probably looking to do 'python featureset_creator.py < urls.txt')\n")
	input() #Overwrite ignored.
	input() #Delay ignored.
	
	print("Not fetching, so ignoring arguments.\n")

	here = path.dirname(path.realpath(__file__))
	songinfo, test_songs = [], []
	random.seed(0)
	for line in sys.stdin:
		line = line.strip()
		if line == '':
			continue
		
		url = line.strip().split(" ")[2]
		
		in_filename = generatefilename(url)
		in_filepath = path.join(here, in_subdir, in_filename)
		
		song = readsong(in_filepath, in_filename, False, False, False) #Booleans are print optionals - first is for errors, second is for standard prints (success print)
		
		if song is not False:
			if random.random() < .1: #10% Test songs
				test_songs.append(TestSong(*song))
			else:
				songinfo.append(song)

	for seed in [0,1]:
		print("Seed:",seed)
		random.seed(seed)
		copy_songinfo = copy.deepcopy(songinfo)
		random.shuffle(copy_songinfo)

		for k in range(5):
			DevSong.yearyeardict = dict()
			DevSong.genredict = dict()
			DevSong.artistdict = dict()
			DevSong.tokendict = dict()
			DevSong.disneycount = 0
			DevSong.nondisneycount = 0

			Song0.yeardict = dict()
			Song0.genredict = dict()
			Song0.artistdict = dict()
			Song0.tokendict = dict()
			Song0.disneycount = 0
			Song0.nondisneycount = 0

			dev_songs = []
			training_songs = []
			for i,song in enumerate(copy_songinfo):
				if i%5 == k:
					dev_songs.append(DevSong(*song))
				else:
					training_songs.append(Song0(*song))


			"""
			print()
			print(f"#Disney songs in training set: {Song0.disneycount}")
			print(f"#Non-Disney songs in training set: {Song0.nondisneycount}")
			print(f"Disney percentage in training set: {round(Song0.disneycount/len(training_songs)*100)} %")

			print()
			
			print(f"#Disney songs in dev set: {DevSong.disneycount}")
			print(f"#Non-Disney songs in dev set: {DevSong.nondisneycount}")
			print(f"Disney percentage in dev set: {round(DevSong.disneycount/len(dev_songs)*100)} %")

			print()
			"""
			most_popular_years = Song0.most_popular('years')
			most_popular_genres = Song0.most_popular('genres')
			most_popular_artists = Song0.most_popular('artists')
			most_popular_tokens = Song0.most_popular('tokens')
			"""
			print(f"#Years in vector: {len(most_popular_years)}")
			print(f"#Genres in vector: {len(most_popular_genres)}")
			print(f"#Artists in vector: {len(most_popular_artists)}")
			print(f"#Tokens in vector: {len(most_popular_tokens)}")
			"""
			print(f"Total length of vector: {len(most_popular_years)+len(most_popular_genres)+len(most_popular_artists)+len(most_popular_tokens)+1}")
			print()
			#print("Sorted:",sorted(list(Song.tokendict.values()), reverse=True)[:max_tokens])
			assert most_popular_years[k] and most_popular_genres and most_popular_artists and most_popular_tokens ##Assert all are not False
			#print(len(most_popular_years), len(most_popular_genres), len(most_popular_artists), len(most_popular_tokens))

			training_set, dev_set = [], []

			for song in training_songs:
				training_set.append( song.vectorize(most_popular_years, most_popular_genres, most_popular_artists, most_popular_tokens)[1] ) #(*years, *genres, *artists, *gender, *tokens), disney)
			
			for devsong in dev_songs:
				dev_set.append( devsong.vectorize(most_popular_years, most_popular_genres, most_popular_artists, most_popular_tokens)[1] ) #(*years, *genres, *artists, *gender, *tokens), disney)
			

			with open("featuresubset"+str(seed)+"_"+str(k)+".pickle","wb") as featuresubset_f:
				pickle.dump(training_set, featuresubset_f)
			print("featuresubset"+str(seed)+"_"+str(k)+".pickle created.")

			with open("dev_featuresubset"+str(seed)+"_"+str(k)+".pickle","wb") as dev_featuresubset_f:
				pickle.dump(dev_set, dev_featuresubset_f)
			print("dev_featuresubset"+str(seed)+"_"+str(k)+".pickle created.")

		print()
	
	#///#

	all_training_songs = []

	for song in songinfo:
		all_training_songs.append(Song(*song))

	most_popular_years = Song.most_popular('years')
	most_popular_genres = Song.most_popular('genres')
	most_popular_artists = Song.most_popular('artists')
	most_popular_tokens = Song.most_popular('tokens')

	print(f"#Years in vector: {len(most_popular_years)}")
	print(f"#Genres in vector: {len(most_popular_genres)}")
	print(f"#Artists in vector: {len(most_popular_artists)}")
	print(f"#Tokens in vector: {len(most_popular_tokens)}")
	print(f"Total length of vector: {len(most_popular_years)+len(most_popular_genres)+len(most_popular_artists)+len(most_popular_tokens)+1}")

	all_training_sets = []

	for song in all_training_songs:
		all_training_sets.append( song.vectorize(most_popular_years, most_popular_genres, most_popular_artists, most_popular_tokens)[1] ) #(*years, *genres, *artists, *gender, *tokens), disney)

	with open("training_featuresubsets.pickle","wb") as test_featuresubset_f:
				pickle.dump(all_training_sets, test_featuresubset_f)
				print("training_featuresubsets.pickle created.")

	#///#

	named_test_sets = []

	for test_song in test_songs:
		named_test_sets.append( test_song.vectorize(most_popular_years, most_popular_genres, most_popular_artists, most_popular_tokens) ) #(*years, *genres, *artists, *gender, *tokens), disney)
			
	
	test_titles, test_set = [], []

	for test_title, test_featureset in named_test_sets:
		test_titles.append(test_title)
		test_set.append(test_featureset)

	with open("test_featuresubsets.pickle","wb") as test_featuresubset_f:
			pickle.dump(test_set, test_featuresubset_f)
			print("test_featuresubsets.pickle created.")

	with open("test_titles.pickle","wb") as test_titles_f:
			pickle.dump(test_titles, test_titles_f)
			print("test_titles.pickle created.")