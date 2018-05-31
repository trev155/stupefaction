import spacy


def pos_tagging_example():
    doc = nlp("Apple is looking at buying U.K. startup for $1 billion.")
    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_)


def noun_chunking_example():
    doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_, chunk.root.head.text)


def named_entities_example():
    doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)


def sentence_segmentation_example():
    doc = nlp("This is a sentence. This is another sentence.")
    for sent in doc.sents:
        print(sent.text)


if __name__ == "__main__":
    nlp = spacy.load("en_core_web_sm")

    # pos_tagging_example()
    # noun_chunking_example()
    # named_entities_example()
    sentence_segmentation_example()
