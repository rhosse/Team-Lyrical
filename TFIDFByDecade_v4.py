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

#letter = "P"
#filename = "%s" % letter+ "_LyricWikia(2).csv" # Use LyricWikia data as its years are more comprehensive

filename = "_LW_ConcatCSVs.csv"

# Compile only the year (fused into 5-year intervals) and lyrics (Note: These inputs can be modified if different metadata
# is sought (e.g. artists/genres instead of time periods))

rawLyrics = []
allTimePeriods = ['1950-1959','1960-1964','1965-1969','1970-1974','1975-1979','1980-1984','1985-1989','1990-1994',\
                  '1995-1999','2000-2004','2005-2009','2010-2014','2015-2019']
with open(filename,'rt') as lyricFile:
    lyricReader = csv.reader(lyricFile)
    next(lyricReader, None) # skip header
    for row in lyricReader:
        try:
            lyric = row[3].lower()
            if float(row[1]) >= 1950 and float(row[1]) <= 1959:
                rawLyrics.append(('1950-1959',lyric))
            elif float(row[1]) >= 1960 and float(row[1]) <= 1964:
                rawLyrics.append(('1960-1964',lyric))
            elif float(row[1]) >= 1965 and float(row[1]) <= 1969:
                rawLyrics.append(('1965-1969',lyric))
            elif float(row[1]) >= 1970 and float(row[1]) <= 1974:
                rawLyrics.append(('1970-1974',lyric))
            elif float(row[1]) >= 1975 and float(row[1]) <= 1979:
                rawLyrics.append(('1975-1979',lyric))
            elif float(row[1]) >= 1980 and float(row[1]) <= 1984:
                rawLyrics.append(('1980-1984',lyric))
            elif float(row[1]) >= 1985 and float(row[1]) <= 1989:
                rawLyrics.append(('1985-1989',lyric))
            elif float(row[1]) >= 1990 and float(row[1]) <= 1994:
                rawLyrics.append(('1990-1994',lyric))
            elif float(row[1]) >= 1995 and float(row[1]) <= 1999:
                rawLyrics.append(('1995-1999',lyric))
            elif float(row[1]) >= 2000 and float(row[1]) <= 2004:
                rawLyrics.append(('2000-2004',lyric))
            elif float(row[1]) >= 2005 and float(row[1]) <= 2009:
                rawLyrics.append(('2005-2009',lyric))
            elif float(row[1]) >= 2010 and float(row[1]) <= 2014:
                rawLyrics.append(('2010-2014',lyric))
            elif float(row[1]) >= 2015:
                rawLyrics.append(('2015-2019',lyric))
            else:
                pass
        except:
            pass

# For every time period, consolidate *all* lyrics (from all songs) into a single string, then combine that string into a tuple
# with the time period
# Insert code that read rawLyrics from a file
#with open('rawLyrics.csv') as f:
#    rawLyrics = f.read().splitlines()

# For every time period, consolidate *all* lyrics (from all songs) into a single string, then combine that string into a tuple
# with the time period

print('Initialize the lyricsByPeriod array ...')
allLyrics = ["","","","","","","","","","","","",""]
songCount = [0,0,0,0,0,0,0,0,0,0,0,0,0]
print('Start for loop for allTimePeriods ...')
for idx2, song in enumerate(rawLyrics):
	if idx2 % 100 == 0:
		print("Going through song %d of %d after %f s: " % (idx2, len(rawLyrics), time.time()-start))
	
	if song[0] == '1950-1959':
		idx = 0
	elif song[0] == '1960-1964':
		idx = 1
	elif song[0] == '1965-1969':
		idx = 2
	elif song[0] == '1970-1974':
		idx = 3
	elif song[0] == '1975-1979':
		idx = 4
	elif song[0] == '1980-1984':
		idx = 5
	elif song[0] == '1985-1989':
		idx = 6	
	elif song[0] == '1990-1994':
		idx = 7
	elif song[0] == '1995-1999':
		idx = 8
	elif song[0] == '2000-2004':
		idx = 9
	elif song[0] == '2005-2009':
		idx = 10
	elif song[0] == '2010-2014':
		idx = 11
	else:
		idx = 12
	
	songCount[idx] += 1
	allLyrics[idx] = allLyrics[idx] + " " + song[1]
	
lyricsByPeriod = []
for idx, period in enumerate(allTimePeriods):
	lyricsByPeriod.append((period,allLyrics[idx]))


# Insert code that writes the list lyricsByPeriod to a file
#lyricsByPeriod = []
#for period in allTimePeriods:
#    allLyrics = ""
#    for song in rawLyrics:
#        if song[0] == period:
#            allLyrics = allLyrics+" "+song[1] # NEED A SPACE HERE OTHERWISE YOU GET FUSED WORDS WHEN YOU JOIN LYRICS
#        else:
#            pass
#    lyricsByPeriod.append((period,allLyrics))

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
    for word in list(recordCount): # Remove words from the dictionary with counts of less than 3 (increase for larger sets)
        if recordCount[word] < 10:
            del recordCount[word]
        else:
            pass
    return recordCount

# Iterate the Dictionary Builder function across all time periods and create a new list of tuples pairing each decade with
# its associated lexicon

periodLexicon = []
for period in lyricsByPeriod:
    lexicon = dictBuilder(period[1])
    periodLexicon.append((period[0],lexicon))

# Create a list of dictionaries (without the decades, but in the appropriate order) for use in TF-IDF processing defined
# below

lDictList = []
for period in periodLexicon:
    lDictList.append(period[1])

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
TFIDFPeriods = computeTFIDF(tfl,idfl)

#print(TFIDFArtists)

# The following function creates a CSV file

def TwentyLargestTFIDFByComponent(tfd):
    #outfilename = "%s" % letter + "_PeriodTFIDF_LyricWikia.csv" # commented out when assessing the entire data set
    outfilename = "AllRecords_PeriodTFIDF_LyricWikia.csv"
    s=0
    with open(outfilename,'w',newline='') as csvfile:
        resultsWriter = csv.writer(csvfile)
        #resultsWriter.writerow(['Genre', 'Word1', 'Word2', 'Word3', 'Word4', 'Word5', 'Word6', 'Word7', \
        #                        'Word8', 'Word9', 'Word10', 'Score1', 'Score2', 'Score3', 'Score4','Score5', \
        #                        'Score6', 'Score7', 'Score8', 'Score9', 'Score10'])
        resultsWriter.writerow(['Year', 'Word1', 'Word2', 'Word3', 'Word4', 'Word5', 'Word6', 'Word7', \
                                'Word8', 'Word9', 'Word10', 'Word11', 'Word12', 'Word13', 'Word14', 'Word15', \
                                'Word16', 'Word17', 'Word18', 'Word19', 'Word20', 'Score1', 'Score2', 'Score3', \
                                'Score4','Score5', 'Score6', 'Score7', 'Score8', 'Score9', 'Score10', 'Score11', \
                                'Score12', 'Score13', 'Score14', 'Score15', 'Score16', 'Score17', 'Score18', \
                                'Score19', 'Score20'])
        for dictionary in tfd:
            artist = lyricsByPeriod[s][0]
            TwentyLargest = nlargest(20,dictionary,key=dictionary.get) # interchange with TenLargest and replace 20 with 10
            scores = []
            for w in TwentyLargest:
                score = dictionary[w]
                scores.append(score)
            row = [artist]+TwentyLargest+scores
            resultsWriter.writerow(row)
            s=s+1
    csvfile.close()

TwentyLargestTFIDFByComponent(TFIDFPeriods)

print("CSV file written. Completion time %f s" % (time.time()-start))

# Completion time for letter X (1654 KB/1675 records) assessing to 5-year intervals with terms with less than 3 occurrences 
# discarded: NEED TO RE-RUN (previously 10.02 seconds before "testList" corrected)

# Completion time for letter P (37,000 KB/35,258 records) assessing to 5-year intervals with terms with less than 5 
# occurrences discarded: NEED TO RE-RUN (previously 3854.57 seconds before "testList" corrected)

# Completion time for entire LyricWikia Data Set (893,401 KB) assessing to 5-year intervals with terms less than 10
# occurrences discarded: TBD