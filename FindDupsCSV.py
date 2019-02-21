# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 20:33:16 2019

FindDupsCSV: Review the input CSV music files processed by CleanCSV and 
             perform the following tasks:
1. Read in cleaned (2) file row-by-row into a list
2. Call FindDup to check for duplicate lyrics AND matching group names. 
   If found return True, otherwise return False.
3. IF True returned, write row list to DupCSVList
4. If False returned, write row list to outputCSV_list
5. When finished reading all rows from input file, write outputCSV_list to 
   <inputfilename>(3).csv
6. Write duplicate rows in DupCSVList to <inputfilename>(3-Dups).csv
7. Output record counts saved and duplicated to the console

NOTE: Before running script, install langdetect using pip:
         pip install langdetect
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

def FindDup(value, seq, index):
    ''' First version Find Dup: Check only lyrics 
    Locate and return a boolean indicating if a match based on the value
    passed and the sequence list indexed by the parameter index. These 
    parameters allow for completely flexible checking.'''
    
    Match = False
    for item in seq:
        if item[index] == value:
            Match = True
            break
    return Match

def FindDup2(value, seq, index, band, index2):
    ''' Second version, checks both lyrics and band name.
    Locate and return a boolean indicating if a match based on the value
    passed and the sequence list indexed by the parameter index. These 
    parameters allow for completely flexible checking.'''
    
    Match = False
    for item in seq:
        if item[index] == value and str(item[index2]).lower() == str(band).lower():
            Match = True
            break
    return Match
    
def RemoveDups(seq): 
   # Preserve sequence 
   print("Checking and removing duplicates")
   seen = [] 
   for item in seq: # Process all songs
       if item in seen: 
           continue # Match across all fields found, don't save
       seen.append(item)
   print("Done checking")
   return seen

def main():

    input_filename = ""
    if len(sys.argv) > 1:
        env = sys.argv
        input_filename = str(env[1]) # Assume only one parameter, input filename
        output_filename = input_filename.replace("(2).csv", "(3).csv", 1)
        output_Dups_filename = output_filename.replace("(3).csv", "(3-Dups).csv",1) 
        start = datetime.now()
        print(str(start) + " Start FindDupsCSV Ver. 1")
        print("Reading: " + input_filename + ", Writing: " + output_filename)
		
        # Read columns Artist,Genre,Band Popularity,Song,Year,Song Popularity,Lyrics
        with open(input_filename, 'rb') as csvfileInput:
            
            inputCSV_list = csvfileInput.readlines()
            csvfileInput.close()
            outputCSV_list = [['Artist','Genre','Band Popularity','Song','Year','Song Popularity','Lyrics']]
            DupCSVList = []
            
            with open(output_filename, 'w', newline='') as csvfileOutput:
                csvwrite = csv.writer(csvfileOutput)
                
                for row in inputCSV_list:
                    if killer.kill_now == True:
                        print("exit_state TRUE")
                        break
                    try:
                        values = row.decode('ascii').rstrip().split(',')
                        # Check here if duplicates present, if duplicate found 
                        # save in a seperate list
                        if FindDup2(values[6], outputCSV_list,6,values[0],0) == True:
                            DupCSVList.append(values)
                        else:    
                            outputCSV_list.append(values)

                    except: # Error encountered decoding lyrics, get next song
                        continue 
                # Only write outputCSV_list AFTER for loop complete!
                csvwrite.writerows(outputCSV_list) 

        if len(DupCSVList) > 1: # Check if duplicates found
            with open(output_Dups_filename, 'w', newline='') as csvfileOutput:
                csvwrite = csv.writer(csvfileOutput)
                csvwrite.writerows(DupCSVList)
            
        end = datetime.now()
        print("\n" + str(end) + " Finished in " + str(end-start) + \
              ", Processed file: " + input_filename + \
              ", Records Saved: " + str(len(outputCSV_list)-1) + \
              ", Duplicate Records: " + str(len(DupCSVList)-1))
    else:
        print("\nUsage: ipython FindDupsCSV.py <CleanedLyricsFile(2).csv>\n")
	
    
if __name__ == '__main__':
    killer = GracefulKiller()
    print('Press Ctrl+C to exit')
    try:
        main()
    except KeyboardInterrupt:
        pass
    