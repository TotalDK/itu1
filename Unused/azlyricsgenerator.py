import csv
a = 0
aa = []
for i in range(0,267):
	try:
		with open(r"Unavngivet regneark - Ark1.csv") as csvfile:
			reader = csv.reader(csvfile)
			test = ([x for x in csv.reader(csvfile)][i])
			artist = str((test[1].lower()))
			songname = str((test[0].split(",")[0].lower()))
			Disney = test[4]
			Gender = test[2]
			print(Disney,Gender,2000,"https://www.azlyrics.com/lyrics/{}/{}.html".format(artist.replace(' ',''),songname.replace(" ","")))
	except:
		pass
		a += 1
	#	print(f"{i:>4}")

"""
import pandas as pd
import numpy as np

data = np.array(pd.read_csv('DisneyPixarDataset.csv', delimiter=','))
print(data[:,0])
"""