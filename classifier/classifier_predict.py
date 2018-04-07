import pickle

import make_data

with open('classifier.p', 'rb') as f:
    classifier = pickle.load(f)

def classify(tags):
    result = []
    for tag in tags:
        result.append(classifier.classify(make_data.prepare_features(tag)))
    return result