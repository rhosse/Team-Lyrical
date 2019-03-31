# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 15:49:17 2019

@author: Philip.Crandon
"""

import csv
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import math
from heapq import nlargest
import time

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
allWords = set(nltk.corpus.words.words()) # NLTK's dictionary of words

start=time.time()

# Specify letter to be used (If assessing the entire data set, remove "letter" and set the filename accordingly)

#letter = "X"
#filename = "%s" % letter+ "(5).csv"

filename = "MetroCombinedLyrics.csv"

# Compile only the genre and lyrics (Note: These inputs can be modified if different metadata is sought (e.g. years
# instead of artists))

rawLyrics = []
allGenres = ['Rock', 'Pop', 'Country', 'Electronic', 'Hip-Hop', 'Metal', 'Folk', 'Jazz', 'Indie']
with open(filename,'rt') as lyricFile:
    lyricReader = csv.reader(lyricFile)
    next(lyricReader, None) # skip header
    for row in lyricReader:
        try:
            lyric = row[6].lower()
            #rawLyrics.append((row[1],lyric))
            #if row[1] not in allGenres:
            #    allGenres.append(row[1])
            if row[1] == 'Rock':
                rawLyrics.append(('Rock',lyric))
            elif row[1] == 'Pop':
                rawLyrics.append(('Pop',lyric))
            elif row[1] == 'Country':
                rawLyrics.append(('Country',lyric))
            elif row[1] == 'Electronic':
                rawLyrics.append(('Electronic',lyric))
            elif row[1] == 'Hip-Hop':
                rawLyrics.append(('Hip-Hop',lyric))
            elif row[1] == 'Metal':
                rawLyrics.append(('Metal',lyric))
            elif row[1] == 'Folk':
                rawLyrics.append(('Folk',lyric))
            elif row[1] == 'Jazz':
                rawLyrics.append(('Jazz',lyric))
            elif row[1] == 'Indie':
                rawLyrics.append(('Indie',lyric))
            else:
                pass
        except:
            pass

# For every genre, consolidate *all* lyrics (from all songs) into a single string, then combine that string into a tuple
# with the genre name

print('Initialize the lyricsByGenre array ...')
allLyrics = ["","","","","","","","",""]
songCount = [0,0,0,0,0,0,0,0,0]
print('Start for loop for allGenres ...')
for idx2, song in enumerate(rawLyrics):
	if idx2 % 100 == 0:
		print("Going through song %d of %d after %f s: " % (idx2, len(rawLyrics), time.time()-start))
	
	if song[0] == 'Rock':
		idx = 0
	elif song[0] == 'Pop':
		idx = 1
	elif song[0] == 'Country':
		idx = 2
	elif song[0] == 'Electronic':
		idx = 3
	elif song[0] == 'Hip-Hop':
		idx = 4
	elif song[0] == 'Metal':
		idx = 5
	elif song[0] == 'Folk':
		idx = 6	
	elif song[0] == 'Jazz':
		idx = 7
	elif song[0] == 'Indie':
		idx = 8
	else:
		pass
	
	songCount[idx] += 1
	allLyrics[idx] = allLyrics[idx] + " " + song[1]
	
lyricsByGenre = []
for idx, genre in enumerate(allGenres):
	lyricsByGenre.append((genre,allLyrics[idx]))

# Define a function to generate a dictionary which counts all words in a string, setting the words as keys and counts as 
# values. Apply lemmatization and tokenization, and remove the word "sup" (from html code found to have impacted the results).
# Additional unwanted words can also be removed at this step.
    
# Additionally, issues were found with tokenization in which some words were found to have counts of zero, despite appearing
# in the lyrics. This triggered Key Errors at subsequent steps. As a result, locate words with counts of zero and
# (artificially) raise their count to a nominal one.

def dictBuilder(lyricString):
    stop_free = " ".join([i for i in lyricString.split() if i not in stop])
    punc_free = "".join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    #testTokens = nltk.word_tokenize(normalized)
    #testList = list(set(testTokens))
    testList = normalized.split()
    for word in testList:
        if len(word) <= 2:
            testList.remove(word)
        elif word == "sup":
            testList.remove(word) # This part of the code is where you could remove other unwanted words, e.g. "oooh"
        elif word not in allWords:
            testList.remove(word) # Remove non-English words (misspelled, fused, or gibberish words that often have the
            # highest TF-IDF scores)
        else:
            pass
    recordCount = {}
    for word in testList:
        if word in recordCount:
            recordCount[word] = recordCount[word]+1
        else:
            recordCount[word] = 1
    for word in list(recordCount): # Remove words from the dictionary with counts of less than 5 (increase for larger sets)
        if recordCount[word] < 5:
            del recordCount[word]
        else:
            pass
    return recordCount

# Iterate the Dictionary Builder function across all artists and create a new list of tuples pairing each artist's name
# with their associated lexicon

genreLexicon = []
for genre in lyricsByGenre:
    lexicon = dictBuilder(genre[1])
    genreLexicon.append((genre[0],lexicon))

# Create a list of dictionaries (without the artists' names, but in the appropriate order) for use in TF-IDF processing
# defined below

lDictList = []
for genre in genreLexicon:
    lDictList.append(genre[1])

# The following reference was heavily used for background and for construction of the functions below:
# https://medium.freecodecamp.org/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3

# Define a function that inputs a list of dictionaries (each dictionary with keys as words and values as counts; in this case
# the entire lyrical output of each artist) and generates a list of dictionaries that provides the Term Frequency of each
# word in the context of its respective record/dictionary

def computeTF(dictList):
    tfDictList = []
    s=0
    for d in dictList:
        tfDict = {}
        totalWords = sum(d.values())
        for word in d:
            tfDict[word] = d[word]/totalWords
        tfDictList.append(tfDict)
        s=s+1
    return tfDictList

# Define a function that inputs the same list of dictionaries and returns a single dictionary that provides the Inverse Data
# Frequency for each word, assessing over all records/dictionaries

def computeIDF(dictList):
    idfDict = {}
    N = len(dictList)
    for d in dictList:
        for word in d:
            if d[word]>0:
                if word in idfDict:
                    idfDict[word] = idfDict[word]+1
                else:
                    idfDict[word] = 1
            else:
                pass
    for word,val in idfDict.items():
        idfDict[word] = math.log10(N/float(val))
    return idfDict

# Define a function that uses the outputs of the TF and IDF functions to generate TF-IDF scores for each word in the context
# of its respective record/dictionary

def computeTFIDF(t,i):
    tfIDFDictList = []
    s = 0
    for d in t:
        tfIDFDict = {}
        for word in d:
            tfIDFDict[word] = d[word]*i[word]
        tfIDFDictList.append(tfIDFDict)
        s=s+1
    return tfIDFDictList

# Execute the previously defined TF, IDF, and TF-IDF functions

tfl = computeTF(lDictList)
idfl = computeIDF(lDictList)
TFIDFGenres = computeTFIDF(tfl,idfl)

# The following function creates a CSV file

def TwentyLargestTFIDFByComponent(tfd):
    #outfilename = "%s" % letter + "_GenreTFIDF_MetroCombinedLyrics.csv"
    outfilename = "AllRecords_GenreTFIDF_MetroCombinedLyrics.csv"
    s=0
    with open(outfilename,'w',newline='') as csvfile:
        resultsWriter = csv.writer(csvfile)
        #resultsWriter.writerow(['Genre', 'Word1', 'Word2', 'Word3', 'Word4', 'Word5', 'Word6', 'Word7', \
        #                        'Word8', 'Word9', 'Word10', 'Score1', 'Score2', 'Score3', 'Score4','Score5', \
        #                        'Score6', 'Score7', 'Score8', 'Score9', 'Score10'])
        resultsWriter.writerow(['Genre', 'Word1', 'Word2', 'Word3', 'Word4', 'Word5', 'Word6', 'Word7', \
                                'Word8', 'Word9', 'Word10', 'Word11', 'Word12', 'Word13', 'Word14', 'Word15', \
                                'Word16', 'Word17', 'Word18', 'Word19', 'Word20', 'Score1', 'Score2', 'Score3', \
                                'Score4','Score5', 'Score6', 'Score7', 'Score8', 'Score9', 'Score10', 'Score11', \
                                'Score12', 'Score13', 'Score14', 'Score15', 'Score16', 'Score17', 'Score18', \
                                'Score19', 'Score20'])
        for dictionary in tfd:
            genre = lyricsByGenre[s][0]
            TwentyLargest = nlargest(20,dictionary,key=dictionary.get) # interchange with TenLargest and replace 20 with 10
            scores = []
            for w in TwentyLargest:
                score = dictionary[w]
                scores.append(score)
            row = [genre]+TwentyLargest+scores
            resultsWriter.writerow(row)
            s=s+1
    csvfile.close()

TwentyLargestTFIDFByComponent(TFIDFGenres)

print("CSV file written. Completion time %f s" % (time.time()-start))

# Completion time for letter X (2735 KB/2086 records) with terms with less than 5 occurrences discarded: TBD

# Completion time for letter P (34,044 KB/25,969 records) with terms with less than 10 occurrences discarded: TBD

# Completion time for entire MetroCombinedLyrics Data Set (677,725 KB) with terms with less than 10 occurrences discarded: 
# TBD