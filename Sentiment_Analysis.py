# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:02:08 2019
Sentiment analysis prototype initialy using A(4).csv

@author: Paul.Devine
"""

# Import needed libraries
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import matplotlib as plt
#%matplotlib inline
import seaborn as sns
from textblob import TextBlob, Word
import signal
import sys
from nltk.corpus import stopwords

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    print('You pressed Ctrl+C!')
    self.kill_now = True


def preprocess(df):
    ''' Perform text preprocessing tasks here '''

    # Make sure all lowercase and remove punctuations
    df['Lyrics'] = df['Lyrics'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    df['Lyrics'] = df['Lyrics'].str.replace('[^\w\s]','')

    # Remove stop words
    stop = stopwords.words('english')
    df['Lyrics'] = df['Lyrics'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))

    # Perform Lemmatization
    df['Lyrics'] = df['Lyrics'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
    return df

def Create_Dict_Total(df, inputkey):
    
    local_dict = {}  # Count positive, negative by genre
    for row in df.iterrows():
        key = str(row[1][inputkey]) + ',' + str(row[1]['VADERSentiment'])
        if key in local_dict:
            local_dict[key] += 1
        else:
            local_dict[key] = 1
        key = str(row[1][inputkey]) + ',' + str(row[1]['BLOBSentiment'])
        if key in local_dict:
            local_dict[key] += 1
        else:
            local_dict[key] = 1
            
    return local_dict

def Create_Ratings_Dict_Total(df, inputkey):

    local_dict = {}  # Count positive, negative by genre
    for row in df.iterrows():
        try:
            if float(row[1][inputkey]) >= 80.:
                key = '80,'
            elif float(row[1][inputkey]) >= 60.:
                key = '60,'
            elif float(row[1][inputkey]) >= 40.:
                key = '40,'
            elif float(row[1][inputkey]) >= 20.:
                key = '20,'
            else:
                key = '00,'
            Vkey = key + str(row[1]['VADERSentiment'])
            if Vkey in local_dict:
                local_dict[Vkey] += 1
            else:
                local_dict[Vkey] = 1
            Bkey = key + str(row[1]['BLOBSentiment'])
            if Bkey in local_dict:
                local_dict[Bkey] += 1
            else:
                local_dict[Bkey] = 1
        except: # if conversion dosen't work read next row
            continue
    return local_dict
            
def Write_To_CSV(total_dict, suffix, outputfilename):
    status = 0  # Write out to specified CSV file
    output_filename = outputfilename.replace(".csv", suffix + ".csv", 1)
    with open(output_filename, 'w', newline='') as outfile:
        for key,value in total_dict.items():
            try:
                outfile.write(str(key) + ',' + str(value) + '\n')
            except:
                status += 1
                continue

def Generate_Sentiment_Scores(df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()

    emptyline = []
    for row in df['Lyrics']:
        vs = analyzer.polarity_scores(row)
        blob = TextBlob(row)        
        vs['polarity'] = blob.polarity
        vs['subjectivity'] = blob.subjectivity
        emptyline.append(vs)
        if killer.kill_now == True:
            print("exit_state TRUE")
            sys.exit()

    df_sentiments = pd.DataFrame(emptyline)
    # Merge sentiments back into lyrics dataframe
    df = pd.concat([df.reset_index(drop=True), df_sentiments], axis=1)
    # Convert scores into positive, negative sentimes using threshold 0.0 
    df['VADERSentiment'] = np.where(df['compound'] >= 0, 'VADER_Positive', 'VADER_Negative')
    # Convert scores into positive, negative sentimes using threshold 0.0 
    df['BLOBSentiment'] = np.where(df['polarity'] >= 0, 'BLOB_Positive', 'BLOB_Negative')

    return df


if __name__ == '__main__':
    killer = GracefulKiller()
    print('Press Ctrl+C to exit')
    try:
        inputCSV_list = []
        output_filename = ""
        # open text file and read artist names, one per line
        if len(sys.argv) > 1:
            env = sys.argv
            input_filename = str(env[1])
            output_filename = str(env[2])
            # open text file and read artist names, one per line
            with open(input_filename, 'rt') as csvfileInput:
                inputCSV_list = csvfileInput.readlines()
                csvfileInput.close()
        else:
            print("\nUsage: python Sentiment_Analysis.py <InpuCSVs.txt> <output.csv>\n")
            sys.exit()

        plt.style.use('fivethirtyeight')
        cp = sns.color_palette()        
        df_total = pd.DataFrame()

        for inputCSV_file in inputCSV_list:
            inputCSV_file = inputCSV_file.strip()
            if len(inputCSV_file) == 0:
                continue
            print("Processing: " + inputCSV_file)
            # Read in lyrics into a data frame 
            df = pd.read_csv(inputCSV_file)
            df.info() # Review info
        
            df = preprocess(df)
            df_total = df_total.append(Generate_Sentiment_Scores(df), ignore_index=True)
    
        total_dict = Create_Dict_Total(df_total, 'Year')
        Write_To_CSV(total_dict, '_Year', output_filename)

        #total_dict = Create_Dict_Total(df_total, 'Genre')
        #Write_To_CSV(total_dict, '_Genre', output_filename)

        #total_dict = Create_Dict_Total(df_total, 'Artist')
        #Write_To_CSV(total_dict, '_Artist', output_filename)

        #total_dict = Create_Dict_Total(df_total, 'pyYear')
        #Write_To_CSV(total_dict, '_pyYear', output_filename)

        #total_dict = Create_Ratings_Dict_Total(df_total, 'Band Popularity')
        #Write_To_CSV(total_dict, '_BandPop', output_filename)

        #total_dict = Create_Ratings_Dict_Total(df_total, 'Song Popularity')
        #Write_To_CSV(total_dict, '_SongPop', output_filename)

    except KeyboardInterrupt:
        pass
