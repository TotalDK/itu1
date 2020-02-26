import sys
from nltk.corpus import names
import nltk
import random

def gender_features(word):
	return {'last_letter': word[-1]}



labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
random.shuffle(labeled_names)

featuresets = [(gender_features(n),gender) for (n,gender) in labeled_names]
train_set, test_set = featuresets[500:],featuresets[:500]

classifier = nltk.NaiveBayesClassifier.train(train_set)


classifier.classify(gender_features("Trinity"))
print(featuresets)


#print(labeled_names)


"""
def number_input(a):
	last_number = a[-1]
	print(last_number)
	if last_number == 1:
		print("1")
	elif last_number != 1:
		print("0")
	return last_number



def main():
	a = (sys.stdin.readlines())
	number_input(a)

if __name__ == '__main__':
	main()




"""






"""
number_list = []
numbers = (sys.stdin.readlines())

for x in numbers:
	try:
		val = int(x)
		print(x,"is an int")
	except ValueError:
		try:
			val = float(x)
			print(x,"is a float")
		except ValueError:
			print('"',x,'"', "is neither an int nor a float")
"""