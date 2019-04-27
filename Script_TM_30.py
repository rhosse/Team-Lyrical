import time
ta = time.time()

import numpy as np
import pandas as pd
import re, nltk, spacy, gensim
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import GridSearchCV
from pprint import pprint
import pyLDAvis
import pyLDAvis.sklearn
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv('Data.csv', delimiter = ',')
df.dropna()
data = df.Lyrics.values.tolist()

with open('data_lemmatized_output','rb') as fp:
    data_lemmatized = pickle.load(fp)

# test sample of data
#len(data_lemmatized)	
#data_lemmatized = data_lemmatized[:5000]

print('vectorizing data')

vectorizer = CountVectorizer(analyzer='word',       
                             min_df=500, 
                             stop_words='english', 
                             lowercase=True,
                             token_pattern='[a-zA-Z0-9]{3,}',
                             max_features=1000,
                            )

data_vectorized = vectorizer.fit_transform(data_lemmatized)

print('vectorizing data complete')
print('performing grid search')
								
#search_params = {'n_components': [12,15,20,25,30]}
search_params = {'n_components': [30]}

lda = LatentDirichletAllocation(max_iter= 10,               # Max learning iterations
                                doc_topic_prior = 1,         #Alpha
                                topic_word_prior = .1,       #Beta
                                learning_offset = 5,
                                learning_method='online',
                                random_state=100,          # Random state
                                batch_size=128,            # n docs in each learning iter
                                evaluate_every = -1,       # compute perplexity every n iters, default: Don't
                                n_jobs = -1,               # Use all available CPUs
                                     )

# Init Grid Search Class
model = GridSearchCV(lda, param_grid=search_params, cv = 5)
# model = GridSearchCV(lda, param_grid=search_params, cv = 5, verbose = 2)
# Do the Grid Search
model.fit(data_vectorized)

print('grid search complete')

best_lda_model = model.best_estimator_    # This identifies the best estimator

best_lda_params = model.best_params_       # This get the parameters of the best estimator
model_log_likelihood = model.best_score_  # higher is better
model_perplexity = best_lda_model.perplexity(data_vectorized) # lower is better

print('Best parameters for the model:')
print(best_lda_params)                    # We just print the best parameters, of which "n_components" is a part
print('Log Likelihood: %s Perplexity: %s' % (model_log_likelihood, model_perplexity))    # Print the scores for the best model, higher likelihood is better

data = df.Lyrics.values.tolist()

# Create Document - Topic Matrix
lda_output = best_lda_model.transform(data_vectorized)

# column names
topicnames = ["Topic" + str(i) for i in range(best_lda_model.n_components)]
#topicnames = ["Topic" + str(i) for i in range(5)] #change the value inside range

# index names
docnames = ["Lyr " + str(i) for i in range(len(data))]

# Make the pandas dataframe
#df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)
df_document_topic = pd.DataFrame(np.round(lda_output, 8), columns=topicnames, index=docnames)

# Get dominant topic for each document
dominant_topic = np.argmax(df_document_topic.values, axis=1)
df_document_topic['dominant_topic'] = dominant_topic

# Styling
def color_green(val):
    color = 'green' if val > .1 else 'black'    
    return 'color: {col}'.format(col=color)

def make_bold(val):
    weight = 700 if val > .1 else 400
    return 'font-weight: {weight}'.format(weight=weight)


# Apply Style
df_document_topics = df_document_topic.head(15).style.applymap(color_green).applymap(make_bold)
df_document_topics

print (lda_output)


df_topic_distribution = df_document_topic['dominant_topic'].value_counts().reset_index(name="Num Documents")
df_topic_distribution.columns = ['Topic Num', 'Num Lyrics']
df_topic_distribution
print(df_topic_distribution)

#pyLDAvis.enable_notebook()
#panel = pyLDAvis.sklearn.prepare(best_lda_model, data_vectorized, vectorizer, mds='tsne')
#panel

# Show top n keywords for each topic
def show_topics(vectorizer, lda_model, n_words):
    keywords = np.array(vectorizer.get_feature_names())
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))
    return topic_keywords

topic_keywords = show_topics(vectorizer, best_lda_model, 100)        

# Topic - Keywords Dataframe
df_topic_keywords = pd.DataFrame(topic_keywords)
df_topic_keywords.columns = ['Word '+str(i) for i in range(df_topic_keywords.shape[1])]
df_topic_keywords.index = ['Topic '+str(i) for i in range(df_topic_keywords.shape[0])]
df_topic_keywords
df_topic_keywords.to_csv('topic_keywords_30.csv', index=False)

tz = time.time()
print("Time elapsed: %s seconds" %(tz-ta))