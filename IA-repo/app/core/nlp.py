import spacy
import subprocess
import sys

try:
    nlp = spacy.load("es_core_news_lg")
except OSError:
    print("Downloading language model for the first time...")
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "es_core_news_lg"])
    nlp = spacy.load("es_core_news_lg")
