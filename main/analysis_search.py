"""
analysis_search.py

Read in the output from twitter_search.py, and run some analytics, plot some graphs, etc.
"""
import argparse
import json
import os
import plots

FILE_DELIMITER_CHAR = "|"


###########
# Helpers #
###########
def get_hashtag_counts(data_entries):
    """
    Count the number of occurrences of every hashtag in data_entries.
    :param data_entries: list of data entries
    :return: dictionary of counts
    """
    counts = {}
    for entry in data_entries:
        for hashtag in entry["hashtags"]:
            if hashtag in counts:
                counts[hashtag] += 1
            else:
                counts[hashtag] = 1
    return counts


def get_source_counts(data_entries):
    """
    Count the number of each source for every entry in data_entries.
    :param data_entries: list of data entries
    :return: dictionary of counts
    """
    counts = {}
    for entry in data_entries:
        source = entry["source"]
        if source in counts:
            counts[source] += 1
        else:
            counts[source] = 1
    return counts


def get_pos_tag_counts(data_entries):
    """
    Count the number of part of speech tags in total for all data entries.

    :param data_entries: list of data entries
    :return: dictionary of counts
    """
    counts = {}
    for entry in data_entries:
        for tag in entry["tags"]:
            part_of_speech = tag[1]
            if part_of_speech in counts:
                counts[part_of_speech] += 1
            else:
                counts[part_of_speech] = 1

    return counts


def get_sentiment_counts(data_entries):
    """
    Each data entry has a sentiment score. Classify data entries as positive, negative, neutral, etc.

    :param data_entries: list of data entries
    :return: dictionary of counts
    """
    counts = {}
    for entry in data_entries:
        polarity_score = entry["polarity"]
        if polarity_score <= -0.6:
            sentiment = "very negative"
        elif polarity_score < -0.2:
            sentiment = "negative"
        elif polarity_score < 0.2:
            sentiment = "neutral"
        elif polarity_score < 0.6:
            sentiment = "positive"
        else:
            sentiment = "very positive"

        if sentiment in counts:
            counts[sentiment] += 1
        else:
            counts[sentiment] = 1
    return counts


def get_sent_subj_data(data_entries):
    """
    Get both the polarity and subjectivity scores for all data entries.
    Return as a list of tuples, [(polarity, subjectivity)]

    :param data_entries: list of data entries
    :return: list of tuples
    """
    all_data = []
    for entry in data_entries:
        all_data.append((entry["polarity"], entry["subjectivity"]))
    return all_data


###########
# Helpers #
###########
def title_builder(main, query, date):
    """
    Build a string for a plot title.

    :param main: Main substance of the title.
    :param query: the query used
    :param date: timestamp
    :return: string, a plot title
    """
    return main + ", for the search query '" + query + "', " + "for the last 7 days starting at (" + date + ")"


def get_pos_name(tag):
    """
    Return a string denoting the name of the tag.
    :param tag: string, part-of-speech tag short-form name
    :return: string, part-of-speech short-form + descriptor
    """
    mappings = {
        'CC': 'Coordinating conj.',
        'CD': 'Cardinal num.',
        'DT': 'Determiner',
        'EX': 'Existential there',
        'FW': 'Foreign word',
        'IN': 'Prep. or subord. conj.',
        'JJ': 'Adjective',
        'JJR': 'Adjective, compar.',
        'JJS': 'Adjective, super.',
        'LS': 'List item',
        'MD': 'Modal',
        'NN': 'Noun, sing./mass',
        'NNS': 'Noun, plural',
        'NNP': 'Proper noun, sing.',
        'NNPS': 'Proper noun, plural',
        'PDT': 'Predeterminer',
        'POS': 'Possessive end',
        'PRP': 'Personal pron.',
        'PRP$': 'Possessive pron.',
        'RB': 'Adverb',
        'RBR': 'Adverb, compar.',
        'RBS': 'Adverb, superl.',
        'RP': 'Particle',
        'SYM': 'Symbol',
        'TO': 'to',
        'UH': 'Interjection',
        'VB': 'Verb, base form',
        'VBD': 'Verb, past tense',
        'VBG': 'Verb, present part.',
        'VBN': 'Verb, past part.',
        'VBP': 'Verb, sing.pres.non-3rd',
        'VBZ': 'Verb, sing.pres.3rd',
        'WDT': 'Wh-determiner',
        'WP': 'Wh-pronoun',
        'WP$': 'Possess. wh-pron',
        'WRB': 'Wh-adverb'
    }

    if tag not in mappings:
        return tag
    else:
        return mappings[tag]


if __name__ == "__main__":
    # command line parsing
    parser = argparse.ArgumentParser(description="Preprocess CSV files")
    parser.add_argument("-i", "--input", help="Specify input file path", required=True)
    parser.add_argument("-o", "--output", help="Specify output file path", required=True)
    args = parser.parse_args()

    input_filepath = args.input

    # retrieve the original query used in the search
    basename = os.path.basename(input_filepath)

    query_list = basename.split(FILE_DELIMITER_CHAR)[:-1]
    query_used = " ".join(query_list)

    # retrieve the timestamp
    timestamp = basename.split(FILE_DELIMITER_CHAR)[-1]

    # determine where output files should be placed
    output_filepath = os.path.join(args.output, basename)

    with open(input_filepath, "r") as input_file:
        # read in data as a list of dictionaries
        data_entries = list(map(lambda e: json.loads(e), input_file.readlines()))

        # bar graph of hashtag frequencies
        hashtag_counts = get_hashtag_counts(data_entries)
        plots.create_bar_graph(hashtag_counts, 12, "Hashtags", 0.15,
                               title_builder("Hashtag frequencies", query_used, timestamp),
                               output_filepath + "-hashtags")

        # pie chart of source frequencies
        source_counts = get_source_counts(data_entries)
        plots.create_pie_chart(source_counts, 7, title_builder("Source of Tweets", query_used, timestamp),
                               output_filepath + "-sources")

        # bar graph of part-of-speech frequencies. for parts of speech, also get name mappings
        pos_counts = get_pos_tag_counts(data_entries)
        pos_counts = dict(map(lambda kv: (get_pos_name(kv[0]), kv[1]), pos_counts.items()))
        plots.create_bar_graph(pos_counts, 12, "Part-of-speech Tags", 0.15,
                               title_builder("Part-of-speech Tag Frequencies", query_used, timestamp),
                               output_filepath + "-postags")

        # pie chart for sentiment scores
        sentiment_counts = get_sentiment_counts(data_entries)
        plots.create_pie_chart_fixed_pieces(sentiment_counts,
                                            title_builder("Sentiment Ratings", query_used, timestamp),
                                            output_filepath + "-sentiment")

        # scatter plot for sentiment and subjectivity
        sent_subj_data = get_sent_subj_data(data_entries)
        plots.create_scatter_plot(sent_subj_data,
                                  title_builder("Polarity and Subjectivity", query_used, timestamp),
                                  "Polarity", "Subjectivity", output_filepath + "-sentsubj")
