import random

def prepare_features(tag):
    features = {}
    features['first_letter'] = tag.lower()[0]
    features['last_letter'] = tag.lower()[-1]
    for letter in 'abcdefghijklmnopqqrstuvwxyz':
        features['count({})'.format(letter)] = tag.lower().count(letter)
        features['has({})'.format(letter)] = (letter in tag.lower())
    return features

def create_train_set(files):
    g_set = []

    for file in files:
        data = open(file, 'r').readlines()
        temp = [(prepare_features(line), file.split('.')[0]) for line in data]
        g_set.extend(temp)

    random.shuffle(g_set)
    return g_set[:int(0.7)*len(g_set)], g_set[int(0.3)*len(g_set):]