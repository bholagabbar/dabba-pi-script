import pickle

import nltk

import make_data

train_files = ['biodegradable.txt', 'nonbiodegradable.txt']

train_data, test_data = make_data.create_train_set(train_files)

classifier = nltk.NaiveBayesClassifier.train(train_data)

print "Classifier Accuracy: {}".format(nltk.classify.accuracy(classifier, train_data))

with open('classifier.p', 'wb') as f:
    pickle.dump(classifier, f)

