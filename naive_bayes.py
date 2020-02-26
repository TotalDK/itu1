import nltk
import pickle
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode
from os import path



class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifiers = classifiers
        
    def classify(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)
        
    def confidence(self, features):
        votes = []
        for c in self._classifiers:
            v = c.classify(features)
            votes.append(v)
            
        choice_votes = votes.count(mode(votes))
        conf = choice_votes / len(votes)
        return conf

		
feature = open('featuresets.pickle', 'rb')
featuresets = pickle.load(feature)


training_set = featuresets[:int(0.6*len(featuresets))]
testing_set = featuresets[int(0.6*len(featuresets)):]

ow = ""
if path.isfile("model.pickle"):
    while ow != "y" and ow != "n":
        ow = input("File 'model.pickle' detected. Overwrite? [y/n]").lower()
if ow == "n":
    with open('model.pickle', 'rb') as model_f:
        classifier = pickle.load(model_f)
else:
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    with open('model.pickle', 'wb') as model_f:
        pickle.dump(classifier, model_f)





print('Original Naive Bayes Algo accuarcy percent:', (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

#MultinomialNB
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print('MNB_classifier accuarcy percent:', (nltk.classify.accuracy(MNB_classifier, testing_set))*100)

#BernoulliNB
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print('BNB_classifier accuarcy percent:', (nltk.classify.accuracy(BNB_classifier, testing_set))*100)

#SGDClassifier
SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
SGDClassifier_classifier.train(training_set)
print('SGDClassifier_classifier accuarcy percent:', (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

#SVC
SVC_classifier = SklearnClassifier(SVC())
SVC_classifier.train(training_set)
print('SVC_classifier accuarcy percent:', (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

#LinearSVC
LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(training_set)
print('LinearSVC_classifier accuarcy percent:', (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

#NuSVC
NuSVC_classifier = SklearnClassifier(NuSVC())
NuSVC_classifier.train(training_set)
print('NuSVC_classifier accuarcy percent:', (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)


voted_classifier = VoteClassifier(classifier, MNB_classifier, BNB_classifier, SGDClassifier_classifier, SVC_classifier, LinearSVC_classifier, NuSVC_classifier)

print('voted_classifier accuarcy percent:', (nltk.classify.accuracy(voted_classifier, testing_set))*100)



"""
print('Classification:', voted_classifier.classify(testing_set[0][0]), 'Confidence %:', voted_classifier.confidence(testing_set[0][0])*100)
print('Classification:', voted_classifier.classify(testing_set[1][0]), 'Confidence %:', voted_classifier.confidence(testing_set[1][0])*100)
print('Classification:', voted_classifier.classify(testing_set[2][0]), 'Confidence %:', voted_classifier.confidence(testing_set[2][0])*100)
print('Classification:', voted_classifier.classify(testing_set[3][0]), 'Confidence %:', voted_classifier.confidence(testing_set[3][0])*100)
print('Classification:', voted_classifier.classify(testing_set[4][0]), 'Confidence %:', voted_classifier.confidence(testing_set[4][0])*100)
print('Classification:', voted_classifier.classify(testing_set[5][0]), 'Confidence %:', voted_classifier.confidence(testing_set[5][0])*100)
"""