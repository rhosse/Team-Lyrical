TFIDFByDecade.py (and sister file TFIDFAllArtists_v2.py)

These scripts do the following:
1) Read a selected input file (CSV)
2) Narrow the input data down to the lyrics and one selected metadata field (time period or artist)
3) Join all lyrical records associated with each unique metadata field (i.e. an individual time period or artist) into a giant "bag of words" (e.g. if you have 10 lyrics associated with one artist, they will be joined into single lyrical record for that artist. This record will contain all 10 lyrics and will be unbroken.)
4) Count all words in each "bag of words" and generate a dictionary of word counts
5) Compute TF for each term in relation to its respective "bag of words"
6) Compute IDF for each term in relation to the entire corpus
7) Compute TF-IDF for each term in relation to its respective "bag of words"
8) Identify the top 10 highest TF-IDF scores (indicating unique terms) for each time period or artist and write the results to a CSV file.

TF and IDF computations were done manually as opposed to using built-in functions (such as Scikit-Learn). A significant reference used for developing these scripts is "How to process textual data using TF-IDF in Python" on freeCodeCamp (via Medium), located online at https://medium.freecodecamp.org/how-to-process-textual-data-using-tf-idf-in-python-cd2bbc0a94a3

-------------------------
Input/Output Instructions
-------------------------

For both scripts, specify an input filename on Line 28 OR for letter-dependent filenames, specify a letter on Line 25 and associated filepath on Line 26. (In TFIDFByDecade.py the former is open while the latter is commented out, while in TFIDFAllArtist_v2.py the reverse is true.)

Additionally, the output filename is specified on lines 194/195 in TFIDFByDecade.py and lines 171/172 in TFIDFAllArtists_v2.py. Use the same output file (letter-dependent or letter-independent) as specified for the input file lines.

----------------
Completion Times (on a standard machine running Spyder)
----------------
TFIDFAllArtists_v2.py
- Letter X (1654 KB/1675 records): 4.6 seconds
- Letter P (37,000 KB/35,258 records): 1243.23 seconds (approximately 21 minutes)

TFIDFByDecade.py
- Letter X (1654 KB/1675 records), assessing to 10-year periods: 5.23 seconds
- Letter P (37,000 KB/35,258 records), assessing to 10-year periods: 305.12 seconds (approximately 5 minutes)
- Entire LyricWiki Data Set (893,401 KB), assessing to 5-year periods: 52,906.92 seconds (approximately 14 hours 40 minutes)

If using AWS or another cluster resource, large scale processing will almost certainly proceed much more quickly. 