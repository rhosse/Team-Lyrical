# -*- coding: utf-8 -*-

# MetroLyrics Data Combiner
#
# Brandon Nipper

import os, time
import pandas as pd

start = time.time()

root = "C:/Users/nippebr/Desktop/DAEN 690/LyricWika/Data_Dupes_Removed/"
outFile = "Data_Cleaned_Dupes_Removed.csv"

filenames = []
for path, subdirs, files in os.walk(root):
    for name in files:
        filenames.append(os.path.join(path, name))
        
combined_csv = pd.concat( [ pd.read_csv(f) for f in filenames ] )
combined_csv.to_csv( outFile, index=False )

print(time.time()-start)

del root, start, filenames, path, subdirs, files, name, outFile