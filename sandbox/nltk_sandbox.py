from nltk.classify import NaiveBayesClassifier, DecisionTreeClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

from nltk.tokenize import word_tokenize
from nltk.corpus import movie_reviews


def run_example():
    """
    Example from - http://www.nltk.org/howto/sentiment.html
    """
    # Retrieve provided sample dataset
    n_instances = 100
    subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
    obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]

    # Split the sample dataset into training and test sets, containing both "subj" and "obj" data
    # "subj" data contains subjective reviews of movies, "obj" data contains objective statements about the movies
    train_subj_docs = subj_docs[:80]
    test_subj_docs = subj_docs[80:100]
    train_obj_docs = obj_docs[:80]
    test_obj_docs = obj_docs[80:100]

    training_docs = train_subj_docs + train_obj_docs
    testing_docs = test_subj_docs + test_obj_docs

    # initialize a SentimentAnalyzer
    sentim_analyzer = SentimentAnalyzer()

    all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
    unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)

    sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

    # obtain a feature-value representation of our datasets
    training_set = sentim_analyzer.apply_features(training_docs)
    test_set = sentim_analyzer.apply_features(testing_docs)

    # train classifier on the training set
    trainer = NaiveBayesClassifier.train(training_set)
    classifier = sentim_analyzer.train(trainer, training_set)

    for key, value in sorted(sentim_analyzer.evaluate(test_set).items()):
        print('{0}: {1}'.format(key, value))


def nltk_classifier_example():
    # Step 1 – Training data
    train = [("Great place to be when you are in Bangalore.", "pos"),
             ("The place was being renovated when I visited so the seating was limited.", "neg"),
             ("Loved the ambience, loved the food", "pos"),
             ("The food is delicious but not over the top.", "neg"),
             ("Service - Little slow, probably because too many people.", "neg"),
             ("The place is not easy to locate", "neg"),
             ("Mushroom fried rice was spicy", "pos"),
             ]

    # Step 2
    dictionary = set(word.lower() for passage in train for word in word_tokenize(passage[0]))

    # Step 3 - training data
    t = [({word: (word in word_tokenize(x[0])) for word in dictionary}, x[1]) for x in train]

    # Step 4 – the classifier is trained with sample data
    classifier = NaiveBayesClassifier.train(t)

    test_data = "Manchurian was hot and spicy"
    test_data_features = {word.lower(): (word in word_tokenize(test_data.lower())) for word in dictionary}

    print(classifier.classify(test_data_features))
    classifier.show_most_informative_features()


def movie_reviews_example():
    def word_feats(words):
        return dict([(word, True) for word in words])

    negids = movie_reviews.fileids('neg')
    posids = movie_reviews.fileids('pos')

    negfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'neg') for f in negids]
    posfeats = [(word_feats(movie_reviews.words(fileids=[f])), 'pos') for f in posids]

    negcutoff = int(len(negfeats) * 3 / 4)
    poscutoff = int(len(posfeats) * 3 / 4)

    trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
    testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
    print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

    classifier = NaiveBayesClassifier.train(trainfeats)
    print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
    classifier.show_most_informative_features()


if __name__ == "__main__":
    # run_example()
    # nltk_classifier_example()
    # movie_reviews_example()
    pass


