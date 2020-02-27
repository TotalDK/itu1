import nltk
import pickle
import random
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from statistics import mode, mean
from os import path


if not path.isfile('test_featuresubsets.pickle') or not path.isfile('test_titles.pickle') or not path.isfile('training_featuresubsets.pickle'):
	quit(f"This script needs the files created by 'vectorizer.py' (featuresets, featuresubsets 0-4 and a test_titleset).\nMake sure you run 'vectorizer.py < urls.txt' in console to create them, then run this script again.")
for s in range(2):
	for k in range(5):
		if not path.isfile('dev_featuresubset'+str(s)+"_"+str(k)+'.pickle') or not path.isfile('featuresubset'+str(s)+"_"+str(k)+'.pickle'):
			quit(f"This script needs the files created by 'vectorizer.py' (featuresets, featuresubsets 0-4 and a test_titleset).\nMake sure you run 'vectorizer.py < urls.txt' in console to create them, then run this script again.")



for seed in [10,11]:
	print(f"Seed: {seed}")
	random.seed(seed)

	for classifier_name, classifier in [
			(" (Original) Naive Bayes", nltk.NaiveBayesClassifier ),
			("Multinomial Naive Bayes", SklearnClassifier(MultinomialNB()) ),
			("  Bernoulli Naive Bayes", SklearnClassifier(BernoulliNB()) ),
		]:
		accuracies = []
		
		for s in range(2):
			for k in range(5):

				with open('featuresubset'+str(s)+"_"+str(k)+'.pickle', 'rb') as featuresubset_f:
					training_set = pickle.load(featuresubset_f)

				with open('dev_featuresubset'+str(s)+"_"+str(k)+'.pickle', 'rb') as dev_featuresubset_f:
					dev_set = pickle.load(dev_featuresubset_f)

				if classifier == nltk.NaiveBayesClassifier:
					classifier = classifier.train(training_set)
				else:
					classifier.train(training_set)
				accuracy = nltk.classify.accuracy(classifier, dev_set)
				accuracies.append(round(accuracy, 2))
			print(f"{classifier_name} accuracy:\t(Avg: {round(mean(accuracies), 2)} Diff: {round(max(accuracies)-min(accuracies), 2)}\tMin/Max: {min(accuracies)}/{max(accuracies)})")







with open('training_featuresubsets.pickle', 'rb') as training_featuresubsets_f:
	featuresets = pickle.load(training_featuresubsets_f)

best_classifier = nltk.NaiveBayesClassifier.train(featuresets)



with open('test_featuresubsets.pickle', 'rb') as test_featuresets_f:
	test_set = pickle.load(test_featuresets_f)

with open('test_titles.pickle', 'rb') as test_titleset_f:
	test_names = pickle.load(test_titleset_f)


true_pos, true_neg, false_pos, false_neg = 0, 0, 0, 0
for song, title in zip(test_set, test_names):
	true_value				= song[1]
	classification_value	= best_classifier.classify(song[0])
	
	if (true_value, classification_value) == ("Disney", "Disney"):
		true_pos += 1
	elif (true_value, classification_value) == ("Not Disney", "Not Disney"):
		true_neg += 1
	elif (true_value, classification_value) == ("Disney", "Not Disney"):
		false_neg += 1
	elif (true_value, classification_value) == ("Not Disney", "Disney"):
		false_pos += 1


print()
print("TP\tTN\tFN\tFP")
print(true_pos, true_neg, false_neg, false_pos, sep="\t")

accuracy = (true_pos+true_neg)/(true_pos+true_neg+false_pos+false_neg)	if (true_pos+true_neg+false_pos+false_neg)	!= 0 else -1
precision = true_pos/(true_pos+false_pos)								if (true_pos+false_pos)						!= 0 else -1
recall = true_pos/(true_pos+false_neg)									if (true_pos+false_neg)						!= 0 else -1
f1_score = 2*(precision*recall)/(precision+recall)						if (precision != -1 and recall != 1)		!= 0 else -1
print()
print(f"Accuracy:  {round(accuracy*100):>3}%\t( P(answer=actual) )")
print(f"Precision: {round(precision*100):>3}%\t( P(actual=Disney|anwer=Disney) )")
print(f"Recall:    {round(recall*100):>3}%\t( P(answer=Disney|actual=Disney) )")
print(f"F1 Score:  {round(f1_score*100):>3}%\t( Weighted average of Precision and Recall )")
print()
print("P(actual=Disney|answer=Disney):        ", round(true_pos/(true_pos+false_pos), 2))
print("P(actual=Not Disney|answer=Not Disney):", round(true_neg/(true_neg+false_neg), 2))
print("P(answer=Disney|actual=Disney):        ", round(true_pos/(true_pos+false_neg), 2))
print("P(answer=Not Disney|actual=Not Disney):", round(true_neg/(true_neg+false_pos), 2))
print()
best_classifier.show_most_informative_features(15)