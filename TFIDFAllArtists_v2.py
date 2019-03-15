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

start=time.time()

# Specify letter to be used (If assessing the entire data set, remove "letter" and set the filename accordingly)

letter = "P"
filename = "%s" % letter+ "_LyricWikia(2).csv"

# filename = "_LW_ConcatCSVs.csv"

# Compile only the artist name and lyrics (Note: These inputs can be modified if different metadata is sought (e.g. years
# instead of artists))

rawLyrics = []
allArtists = []
with open(filename,'rt') as lyricFile:
    lyricReader = csv.reader(lyricFile)
    next(lyricReader, None) # skip header
    for row in lyricReader:
        try:
            lyric = row[3].lower()
            rawLyrics.append((row[0],lyric))
            if row[0] not in allArtists:
                allArtists.append(row[0])
            else:
                pass
        except:
            pass

# For every artist, consolidate *all* lyrics (from all songs) into a single string, then combine that string into a tuple
# with the artist's name

lyricsByArtist = []
for artist in allArtists:
    allLyrics = ""
    for song in rawLyrics:
        if song[0] == artist:
            allLyrics = allLyrics+song[1]
        else:
            pass
    lyricsByArtist.append((artist,allLyrics))

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
    testTokens = nltk.word_tokenize(normalized)
    testList = list(set(testTokens))
    for word in testList:
        if len(word) <= 2:
            testList.remove(word)
        elif word == "sup":
            testList.remove(word) # This part of the code is where you could remove other unwanted words, e.g. "oooh"
        else:
            pass
    recordCount = {c: rawLyrics.count(c) for c in testList}
    for word in recordCount:
        if recordCount[word] == 0:
                #print("Word '%s' improperly counted with zero value" % word)
            recordCount[word] = 1 # Some records are improperly counted with zero value, which causes KeyError; set to 1
        else:
            pass
    return recordCount

# Iterate the Dictionary Builder function across all artists and create a new list of tuples pairing each artist's name
# with their associated lexicon

artistLexicon = []
for artist in lyricsByArtist:
    lexicon = dictBuilder(artist[1])
    artistLexicon.append((artist[0],lexicon))

# Create a list of dictionaries (without the artists' names, but in the appropriate order) for use in TF-IDF processing
# defined below

lDictList = []
for artist in artistLexicon:
    lDictList.append(artist[1])

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
TFIDFArtists = computeTFIDF(tfl,idfl)

#print(TFIDFArtists)

# The following function creates a CSV file

def TenLargestTFIDFByComponent(tfd):
    outfilename = "%s" % letter + "_ArtistTFIDF.csv"
    #outfilename = "AllRecords_ArtistTFIDF.csv"
    s=0
    with open(outfilename,'w',newline='') as csvfile:
        resultsWriter = csv.writer(csvfile)
        resultsWriter.writerow(['Artist', 'Word1', 'Word2', 'Word3', 'Word4', 'Word5', 'Word6', 'Word7', 'Word8', 'Word9', 'Word10'])
        for dictionary in tfd:
            artist = lyricsByArtist[s][0]
            TenLargest = nlargest(10,dictionary,key=dictionary.get)
            row = [artist]+TenLargest
            resultsWriter.writerow(row)
            s=s+1
    csvfile.close()

TenLargestTFIDFByComponent(TFIDFArtists)

print("CSV file written. Completion time %f s" % (time.time()-start))

# Completion time for letter X (1654 KB/1675 records): 4.6 seconds

# Completion time for letter P (37,000 KB/35,258 records): 1243.23 seconds (approximately 21 minutes); seems to be a bit
# slower than an earlier test

# Processing time appears to increase exponentially and likely will take at least several hours to go through the entire
# data set (for all letters)