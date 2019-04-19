#!/usr/bin/env python
# coding: utf-8


# In[1]:

# NOTE: Once "spacy" has been installed and before running this script, enter the following command into 
# the the command prompt line, otherwise an error will occur: 

# python -m spacy download en_core_web_sm

# (where "python" is the name of your Python executable e.g. "python.exe" - may also be "py" or "python3")

import pandas as pd
import numpy as np
import re, nltk, spacy, gensim

# Sklearn
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from pprint import pprint

import time

start=time.time()


# In[2]:


# Import Dataset (MetroLyrics CSV)

df = pd.read_csv('MetroCombinedLyrics.csv', delimiter = ',')

print("Filtering and Merging Lyrical Data by Genre. Time since start %f s" % (time.time()-start))

#Use below line if selecting a random sample of data [used for testing]
df = df.sample(n=2000)

#Use the line below to filter by year(s) [Disabled for Genre Search]
#df = df[(df['Year'] >= 1960) & (df['Year'] <= 1969)]
#df = df[(df['Year'] == 1995)]

#Use the line below to filter by Genre [Disabled for Genre Search as we are trying to combine all genres]
#df = df[df['Genre'] == "Country"]

# Drop NA's and all columns except genre and lyrics
df = df.drop(columns=['Artist','Band Popularity','Song','Year','Song Popularity','pyYear','pyLyrics']).dropna()

#print(df.shape)
#df.head(10)

# Merge all lyrics associated with a specific genre
df = df.groupby(['Genre'])['Lyrics'].apply(' '.join).reset_index()

# Drop all rows where Genre is not one of the 11 pre-defined categories (keeping genre tagged as "Other",
# but not keeping genre tagged as anything else or left blank)
badGenres = df[ (df['Genre'] != 'Country') & (df['Genre'] != 'Electronic') & (df['Genre'] != 'Folk')\
               & (df['Genre'] != 'Hip-Hop') & (df['Genre'] != 'Indie') & (df['Genre'] != 'Jazz')\
               & (df['Genre'] != 'Metal') & (df['Genre'] != 'Other') & (df['Genre'] != 'Pop')\
               & (df['Genre'] != 'R&B') & (df['Genre'] != 'Rock') ].index
#print(badGenres)
#print(badGenres.index)
df = df.drop(badGenres)

#print(df)

# Get order of genres (may vary based on execution) and save as list for use in compiling CSV
genreOrder = df['Genre'].tolist()


# In[3]:


# Convert to list
print("Converting Lyrical Data to List. Time since start %f s" % (time.time()-start))

data = df.Lyrics.values.tolist()

#pprint(data[:2])


# In[4]:


#tokenize

print("Tokenizing Lyrical Data. Time since start %f s" % (time.time()-start))

def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
       
data_words = list(sent_to_words(data))

#print(data_words[:2])


# In[5]:


#Lemmatization

print("Lemmatizing Lyrical Data. Time since start %f s" % (time.time()-start))

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        texts_out.append(" ".join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))

    return texts_out

# Initialize spacy 'en_core_web_sm' model, keeping only tagger component (for efficiency)

# Need to ensure the "en_core_web_sm" installation command is executed at this time otherwise the code
# will fail

nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Do lemmatization keeping only Noun, Adj, Verb, Adverb
data_lemmatized = lemmatization(data_words, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])

#print(data_lemmatized[:2])


# In[6]:

print("Executing TF-IDF Vectorizer. Time since start %f s" % (time.time()-start))

#Import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

#Create the transform
vectorizer = TfidfVectorizer(analyzer='word',
                             lowercase=True, 
                             max_df=1.0, 
                             stop_words='english',             # remove stop words
                             token_pattern='[a-zA-Z0-9]{3,}',  # num chars > 3
                             )

#Tokenize and build vocab
#vectorizer.fit(data_lemmatized)
TFIDFOutput = vectorizer.fit_transform(data_lemmatized)

#Summarize
#print(vectorizer.vocabulary_)
#print(vectorizer.idf_[:20])

# Generate dense matrix of all TF-IDF scores by word/document
# Reference: https://www.quora.com/How-does-TfidfVectorizer-work-in-laymans-terms
col = ['feat_'+ i for i in vectorizer.get_feature_names()]
outputMatrix = pd.DataFrame(TFIDFOutput.todense(), columns=col)

#print(outputMatrix)

# In[7]:

print("Organizing Vectorizer Results. Time since start %f s" % (time.time()-start))

# Create dataframe of top words and remove unwanted "feat_"
topWordsSeries = outputMatrix.apply(lambda s: s.abs().nlargest(20).index.tolist(), axis=1)


topWords = pd.DataFrame(topWordsSeries.values.tolist(), columns=['Word1','Word2','Word3','Word4','Word5',\
                        'Word6','Word7','Word8','Word9','Word10','Word11','Word12','Word13','Word14',\
                        'Word15','Word16','Word17','Word18','Word19','Word20'])
    
topWords['Word1'] = topWords['Word1'].str.replace("feat_", '')
topWords['Word2'] = topWords['Word2'].str.replace("feat_", '')
topWords['Word3'] = topWords['Word3'].str.replace("feat_", '')
topWords['Word4'] = topWords['Word4'].str.replace("feat_", '')
topWords['Word5'] = topWords['Word5'].str.replace("feat_", '')
topWords['Word6'] = topWords['Word6'].str.replace("feat_", '')
topWords['Word7'] = topWords['Word7'].str.replace("feat_", '')
topWords['Word8'] = topWords['Word8'].str.replace("feat_", '')
topWords['Word9'] = topWords['Word9'].str.replace("feat_", '')
topWords['Word10'] = topWords['Word10'].str.replace("feat_", '')
topWords['Word11'] = topWords['Word11'].str.replace("feat_", '')
topWords['Word12'] = topWords['Word12'].str.replace("feat_", '')
topWords['Word13'] = topWords['Word13'].str.replace("feat_", '')
topWords['Word14'] = topWords['Word14'].str.replace("feat_", '')
topWords['Word15'] = topWords['Word15'].str.replace("feat_", '')
topWords['Word16'] = topWords['Word16'].str.replace("feat_", '')
topWords['Word17'] = topWords['Word17'].str.replace("feat_", '')
topWords['Word18'] = topWords['Word18'].str.replace("feat_", '')
topWords['Word19'] = topWords['Word19'].str.replace("feat_", '')
topWords['Word20'] = topWords['Word20'].str.replace("feat_", '')

#print(topWords)

# Create dataframe of top scores and append to dataframe
topScores = pd.DataFrame(np.sort(outputMatrix.values)[:,-20:], columns = ['Score20','Score19','Score18',\
                         'Score17','Score16','Score15','Score14','Score13','Score12','Score11','Score10',\
                         'Score9','Score8','Score7','Score6','Score5','Score4','Score3','Score2','Score1'])
    
#print(topScores)


# Join dataframes (including Genre Order) and reorder columns so that scores are increasing
topWordsAndScores = pd.concat([topWords,topScores], axis=1)
topWordsAndScores['Genre'] = genreOrder
#cols = topWordsAndScores.columns.tolist()
cols = ['Genre', 'Word1','Word2','Word3','Word4','Word5','Word6','Word7','Word8','Word9','Word10',\
        'Word11','Word12','Word13','Word14','Word15','Word16','Word17','Word18','Word19','Word20',\
        'Score1','Score2','Score3','Score4','Score5','Score6','Score7','Score8','Score9','Score10',\
        'Score11','Score12','Score13','Score14','Score15','Score16','Score17','Score18','Score19',\
        'Score20']
topWordsAndScores = topWordsAndScores[cols]

#print(topWordsAndScores)

# Export to CSV
print("Exporting to CSV. Time since start %f s" % (time.time()-start))
topWordsAndScores.to_csv("TFIDFByGenre_MetroCombinedLyrics.csv", index=False)

print("Execution complete. Completion time %f s" % (time.time()-start))

# Completion time 47.7 seconds for a sample size of 2000 songs

# Most of the time is spent at the Lemmatizing step 