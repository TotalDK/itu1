import nltk
import random
import pickle
from nltk.tokenize import sent_tokenize, word_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords, state_union, gutenberg, wordnet, movie_reviews
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from nltk.classify import ClassifierI
from statistics import mode




"""
Terms 
    tokanizing - word tokenizers or sentence tokenizers
    lexicon - words and their meanings, ex. 'bull' in inverstor speak is someone who is positive, 'bull' in normal speak is an animal  
    corpora - body of text, ex. medical journals, presidential speeches


part of speech tagging 
    CC      coordinating conjunction
    CD      cardinal digit
    DT      determiner
    EX      existential there (like: “there is” … think of it like “there exists”)
    FW      foreign word
    IN      preposition/subordinating conjunction
    JJ      adjective ‘big’
    JJR     adjective, comparative ‘bigger’
    JJS     adjective, superlative ‘biggest’
    LS      list marker 1)
    MD      modal could, will
    NN      noun, singular ‘desk’
    NNS     noun plural ‘desks’
    NNP     proper noun, singular ‘Harrison’
    NNPS    proper noun, plural ‘Americans’
    PDT     predeterminer ‘all the kids’
    POS     possessive ending parent’s
    PRP     personal pronoun I, he, she
    PRP$    possessive pronoun my, his, hers
    RB      adverb very, silently,
    RBR     adverb, comparative better
    RBS     adverb, superlative best
    RP      particle give up
    TO,     to go ‘to’ the store.
    UH      interjection, errrrrrrrm
    VB      verb, base form take
    VBD     verb, past tense took
    VBG     verb, gerund/present participle taking
    VBN     verb, past participle taken
    VBP     verb, sing. present, non-3d take
    VBZ     verb, 3rd person sing. present takes
    WDT     wh-determiner which
    WP      wh-pronoun who, what
    WP$     possessive wh-pronoun whose
    WRB     wh-abverb where, when
"""


""" tokenizing """
example_text = 'Hello Mr. Smith, how are you doing today? The weather is great and python is awesome.'


#This is sent_tokenize()
#print(sent_tokenize(example_text)) 
    #prints ['Hello Mr. Smith, how are you doing today?', 'The weather is great and python is awesome.']

#This is word_tokenize()
#rint(word_tokenize(example_text)) 
    #prints ['Hello', 'Mr.', 'Smith', ',', 'how', 'are', 'you', 'doing', 'today', '?', 'The', 'weather', 'is', 'great', 'and', 'python', 'is', 'awesome', '.']
    

""" stop words """
example_sentence = 'This is an example showning off stop word filtration.'
strop_words = set(stopwords.words('english'))

words = word_tokenize(example_sentence)
filtered_sentence = []

#for w in words:
#    if w not in strop_words:
#        filtered_sentence.append(w)
        
#print(filtered_sentence)
    #prints ['This', 'example', 'showning', 'stop', 'word', 'filtration', '.']
    
    
""" stemming """
ps = PorterStemmer()

example_words = ['python', 'pythoner', 'pythoning', 'pythoned', 'pythonly']
new_text = 'It is very important to be pythonly while you are pythoning with python. All pythoners have pythoned poorly at least once.'


words_stem = word_tokenize(new_text)

#for w in words_stem: 
#    print(ps.stem(w))
    #prints the stem version of the word

    
""" part of speech tagging, chunking, chinking, named entity recognition"""
#part of speech tagging - POS, creates tuples with a word and a tag (ex. VBD)
#chunking - creates chunks 
#chinking - removes 
#named entity recognition - can recognize if two names are corrolated, note that this has a high chance of false positives 


train_text = state_union.raw('2005-GWBush.txt')
sample_text = state_union.raw('2006-GWBush.txt')

custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try:
        for i in tokenized:
            words = nltk.word_tokenize(i)
            tagged = nltk.pos_tag(words)
            
            #chunkGram =  r"""Chunck: {<.*>+}
            #                         }<VB.?|IN|DT+>{""" # first is chunking, the other is chinking 
            #chunkParser = nltk.RegexpParser(chunkGram)
            #chunked = chunkParser.parse(tagged)
            #chunked.draw() this should print a tree of the chuks
            #print(chunked)
            #print(tagged)
            
            namedEnt = nltk.ne_chunk(tagged)
            namedEnt.draw()
            
            
    except Exception as e:
        print(str(e))

#process_content()



""" lemmatizing """
#defaults to noun, so other should be specified with pos='a' (a is adjective)
lemmatizer = WordNetLemmatizer()
#print(lemmatizer.lemmatize('cats'))
#print(lemmatizer.lemmatize('cacti'))
#print(lemmatizer.lemmatize('geese'))
#print(lemmatizer.lemmatize('rocks'))
#print(lemmatizer.lemmatize('python'))
#print(lemmatizer.lemmatize('best', pos='a'))
#print(lemmatizer.lemmatize('run', 'v'))
#print(lemmatizer.lemmatize('run'))



""" Corpora """
#the file directory with all the text
#mine is placed at search-ms:displayname=Search%20Results%20in%20OS%20(C%3A)&crumb=location:C%3A%5C\nltk_data
sample = gutenberg.raw('bible-kjv.txt')
tok = sent_tokenize(sample)
#print(tok[5:15])



""" wordnet """
#finds synonyms for given word


syns = wordnet.synsets('programs')
#print(syns[0]) #prints Synset('plan.n.01')
#print(syns[0].lemmas()[0].name()) #prints plan
#print(syns[0].definition()) #prints a series of steps to be carried out or goals to be accomplished
#print(syns[0].examples()) #prints ['they drew up a six-step plan', 'they discussed plans for a new bond issue']


synonyms = []
antonyms = []

#for syn in wordnet.synsets('good'):
#    for l in syn.lemmas():
        #print(l)
#        synonyms.append(l.name())
#        if l.antonyms():
#            antonyms.append(l.antonyms()[0].name())

#print(set(synonyms))
#print(set(antonyms))


w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')

#print(w1.wup_similarity(w2)) #comparing w1 to w2 is given in %


""" text classification, words as featuring for learning, naive bayes and pickle """

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






#classifys as one or the other, needs to be labeled as one or the other
#This sounds like what we should do

documents = [(list(movie_reviews.words(fileid)),category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]

random.shuffle(documents)



#print(movie_reviews.words(fileid)[0])
#print(documents[:2])

all_words = []

for w in movie_reviews.words():
    all_words.append(w.lower())

all_words = nltk.FreqDist(all_words)

#print(all_words.most_common(15))
#print(all_words['stupid'])

word_features = list(all_words.keys())[:3000]


def find_features(document):
    words = set(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
        
    return features
    
#print((find_features(movie_reviews.words('neg/cv000_29416.txt'))))

featuresets = [(find_features(rev), category) for (rev, category) in documents]

"""print(featuresets[0])"""


training_set = featuresets[:1900]
testing_set = featuresets[1900:]

#negative data example 
training_set = featuresets[:100]
testing_set = featuresets[100:]



#classifier = nltk.NaiveBayesClassifier.train(training_set)

classifier_f = open('naivebayes.pickle', 'rb')
classifier = pickle.load(classifier_f)
classifier_f.close()


print('Original Naive Bayes Algo accuarcy percent:', (nltk.classify.accuracy(classifier, testing_set))*100)
classifier.show_most_informative_features(15)

#save_classifier = open('naivebayes.pickle', 'wb')
#pickle.dump(classifier, save_classifier)
#save_classifier.close()



""" scikit-learn """
#continuing from before
#this will be using the deafaults that may be good but could be better

#MultinomialNB
MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(training_set)
print('MNB_classifier accuarcy percent:', (nltk.classify.accuracy(MNB_classifier, testing_set))*100)


#GaussianNB (not used in example)
#GNB_classifier = SklearnClassifier(GaussianNB())
#GNB_classifier.train(training_set)
#print('GNB_classifier accuarcy percent:', (nltk.classify.accuracy(GNB_classifier, testing_set))*100)

BernoulliNB
BNB_classifier = SklearnClassifier(BernoulliNB())
BNB_classifier.train(training_set)
print('BNB_classifier accuarcy percent:', (nltk.classify.accuracy(BNB_classifier, testing_set))*100)


#LogisticRegression
#LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
#LogisticRegression_classifier.train(training_set)
#print('LogisticRegression accuarcy percent:', (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)


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


""" combining algos with a vote """
#continuing from before

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








