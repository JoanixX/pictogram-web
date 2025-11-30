import spacy
try:
    nlp = spacy.load("es_core_news_lg")
except OSError:
    print("Downloading language model for the first time...")
    from spacy.cli import download
    download("es_core_news_lg")
    nlp = spacy.load("es_core_news_lg")
