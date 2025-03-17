import re
import spacy
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def textMine(speech_text):
    nlp = spacy.load("en_core_web_sm")
    filler_words = {"uh", "um", "like",'a','an','the' , "you know", "right", "so", "actually", "basically", "yeah", "just"}
    def clean_text(text):
        text = re.sub(r'\b(?:' + '|'.join(filler_words) + r')\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    cleaned_text = clean_text(speech_text)
    doc = nlp(cleaned_text)

    keywords = {token.text.lower() for token in doc if token.pos_ in {"NOUN", "PROPN"}}

    return keywords