'''
data_lemmatization.py
Data lemmatization generator
keeps only noun, adj, verb, adverb
1.  read in Data.csv
2.  tokenize using gensim
3.  run function to lemmatize using SpaCy
4.  send lemmatization to output for input to topic modeling code (e.g., Script_TM_30.py)
'''
import numpy as np
import pandas as pd
import re, nltk, spacy, gensim

# Sklearn
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from pprint import pprint

# Plotting tools
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt
#%matplotlib inline

# Import Dataset

df = pd.read_csv('/home/ubuntu/Data.csv', delimiter = ',')

#df = df.sample(n=500000)
print(df.shape)
df.dropna()

#tokenize

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
       
data_words = list(sent_to_words(data))

print(data_words[:2])

#Lemmatization

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append(" ".join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))
    return texts_out

# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
# Run in terminal: python3 -m spacy download en
#!python spacy download en_core_web_sm
#in cmd line type python -m spacy.en.download all
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Do lemmatization keeping only Noun, Adj, Verb, Adverb
data_lemmatized = lemmatization(data_words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

import pickle
with open('data_lemmatized_output2','wb') as fp:
    pickle.dump(data_lemmatized, fp)

print(data_lemmatized[:2])
