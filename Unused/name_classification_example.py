import nltk
from nltk.corpus import names
import random

def gender_features(word):
	return {'last_letter': word[-1]}

names = ([(name, 'male') for name in names.words('male.txt')] +
		[(name, 'female') for name in names.words('female.txt')])
random.shuffle(names)

featuresets = [(gender_features(n), g) for (n,g) in names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(classifier.classify(gender_features('Neo')))
print(classifier.classify(gender_features('Trinity')))

print(nltk.classify.accuracy(classifier, test_set))

classifier.show_most_informative_features(5)





def gender_features2(name):
	features = {}
	features["firstletter"] = name[0].lower()
	features["lastletter"] = name[-1].lower()
	for letter in 'abcdefghijklmnopqrstuvwxyz':
		features["count(%s)" % letter] = name.lower().count(letter)
		features["has(%s)" % letter] = (letter in name.lower())
	return features

featuresets = [(gender_features2(n), g) for (n,g) in names]
train_set, test_set = featuresets[500:], featuresets[:500]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, test_set))

train_names = names[1500:]
devtest_names = names[500:1500]
test_names = names[:500]

train_set = [(gender_features(n), g) for (n,g) in train_names]
devtest_set = [(gender_features(n), g) for (n,g) in devtest_names]
test_set = [(gender_features(n), g) for (n,g) in test_names]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print(nltk.classify.accuracy(classifier, devtest_set))

errors = []
for (name, tag) in devtest_names:
	guess = classifier.classify(gender_features(name))
	if guess != tag:
		errors.append( (tag, guess, name) )

for (tag, guess, name) in sorted(errors): 
	print('correct=%-8s guess=%-8s name=%-30s' % (tag, guess, name))