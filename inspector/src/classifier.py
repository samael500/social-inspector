# -*- coding: utf-8 -*-

import yaml
import os
import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier
from inspector.settings import DATA_DIR


class Classifier(object):

    """ The classifier class for check are message is positive or negative """

    filenames = ('positive.ru', 'positive.en', 'negative.ru', 'negative.en')
    filename_suffix = '.yaml'

    training_tweets = []
    all_words = []

    def __init__(self, *args, **kwargs):
        self.load_training_data()
        # train classifier
        self.word_features = nltk.FreqDist(self.all_words).keys()
        training_set = nltk.classify.util.apply_features(self.extract_features, self.training_tweets)
        self.classifier = NaiveBayesClassifier.train(training_set)

    @property
    def get_file_path(self):
        """ Return file path to training data files """
        return ((
            os.path.join(DATA_DIR, filename + self.filename_suffix),
            filename.split('.')[0]) for filename in self.filenames)

    def load_training_data(self):
        """ Init classifier training """
        for filepath, sentiment in self.get_file_path:
            try:
                with open(filepath, 'r') as training_file:
                    training_tweets = yaml.load(training_file)
                for tweet in training_tweets:
                    # to filter short words
                    words = [word.lower() for word in tweet.split() if len(word) >= 3]
                    self.training_tweets.append((words, sentiment))
                    self.all_words.extend(words)
            except IOError:
                pass

    def extract_features(self, document):
        document_words = set(document)
        features = dict()
        for word in self.word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    def classify_tweet(self, tweet):
        return self.classifier.classify(self.extract_features(nltk.word_tokenize(tweet)))

    def classify_coord_tweets(self, tweets):
        for tweet in tweets:
            sentiment = self.classify_tweet(tweet[0])
            tweet.append(sentiment)
        return tweets
