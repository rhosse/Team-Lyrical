# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:47:32 2019
CalcCSVTotals: Generate the following statistics using the metadata associated 
               with each lyric record for all cleaned CSV files A(2).csv to 
               Z(2).csv and Numbers(20).csv.

Note: Prototype version to be used in the Spyder IDE to access and display the
the following dictionaries. Have not yet generated useful console or file output.

SongYearDict contains the number of songs for each year 
artistDict contains the number of songs by artist
genreDict contains the number of songs by genre
@author: Paul.Devine
"""

import csv
import sys
from datetime import datetime
import signal

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    print('You pressed Ctrl+C!')
    self.kill_now = True

def updateDict(inputDict, rowList, index):
    key = rowList[index]
    if key in inputDict:
        inputDict[key] += 1
    else:
        inputDict[key] = 1
    return inputDict


def updateDict2(inputDict, rowList, genre, year):
    key = rowList[genre] + ' ' + rowList[year]
    if key in inputDict:
        inputDict[key] += 1
    else:
        inputDict[key] = 1
    return inputDict
    
def updateDictbyRating(inputDict,rowList,rating):
    key = rowList[0] + ',' + rowList[1]
    if float(rowList[rating]) >= 90.:
        if key in inputDict:
            inputDict[key] += 1
        else:
            inputDict[key] = 1
    return inputDict

def main():
    status = 0
    
    print(str(datetime.now()) + " Start CalcCSVTotals")
    if len(sys.argv) > 1:
        env = sys.argv
        input_filename = str(env[1]) # Assume only one parameter, input filename

        # open text file and read artist names, one per line
        with open(input_filename, 'r') as csvfileInput:
            inputCSV_list = csvfileInput.readlines()
            csvfileInput.close()
            # INDEX:         0      1        2           3     4       5            6
            # Read columns Artist,Genre,Band Popularity,Song,Year,Song Popularity,Lyrics            
            for inputCSV_file in inputCSV_list:
                inputCSV_file = inputCSV_file.strip()
                
                with open(inputCSV_file, 'rb') as inputCSV:
                    try:
                        inputCSVrows = inputCSV.readlines()
                    
                        for row in inputCSVrows:
                            if killer.kill_now == True:
                                print("exit_state TRUE")
                                break
                            try:
                                rowList = row.decode('ascii').rstrip().split(',')
                                #rowList = row.split(',')
                                #updateDict(genreDict, rowList, 1)
                                #updateDict(artistDict, rowList, 0)
                                updateDict(SongYearDict, rowList, 4)
                                updateDict(SongpyYearDict, rowList, 7)
                             
                                #updateDict2(genreYearDict,rowList,1,4)
                                #updateDict2(artistYearDict,rowList,0,4)
                             
                                #updateDictbyRating(artistbyRatingGenre,rowList,5)
                                #updateDictbyRating(artistbyRating2Genre,rowList,2)
 
                            except:
                                status += 1
                                continue
                    except:
                        status += 1
                        continue
                    
    else:
        print("\nUsage: python CalcCSVTotals.py InpuCSVs.txt\n")
    return status

if __name__ == '__main__':
    killer = GracefulKiller()
    print('Press Ctrl+C to exit')
    try:
        
        genreDict = {}
        SongYearDict = {}
        SongpyYearDict = {}
        artistDict = {}
        genreYearDict = {}
        artistYearDict = {}
        artistbyRatingGenre = {}
        artistbyRating2Genre = {}
        artistbyRatingYear = {}
        status = main()
        new_dict = {}
        for key, value in SongYearDict.items():
            new_dict[key] = value
        for key, value in SongpyYearDict.items():
            if key in new_dict:
                new_dict[key] = [new_dict[key], value]
            else:
                new_dict[key] = [0, value]
        status = 0
        with open('YearTotals.csv', 'w', newline='') as outfile:
            for key,value in new_dict.items():
                try:
                    outfile.write(str(key) + ',' + str(value[0]) + ',' + str(value[1]) + '\n')
                except:
                    status += 1
                    continue
                
    except KeyboardInterrupt:
        pass
    