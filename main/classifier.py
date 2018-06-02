from nltk.corpus import movie_reviews
from textblob.classifiers import NaiveBayesClassifier


def train_classifier():
    posids = movie_reviews.fileids('pos')
    negids = movie_reviews.fileids('neg')
    sentences_positive = [(" ".join(movie_reviews.words(fileids=[id])), "pos") for id in posids]
    sentences_negative = [(" ".join(movie_reviews.words(fileids=[id])), "neg") for id in negids]

    training_sentences = sentences_positive + sentences_negative

    classifier = NaiveBayesClassifier(training_sentences)

    return classifier
