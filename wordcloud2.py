# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:54:03 2019

@author: Philip.Crandon
"""

# This script:
# (1) ingests the output CSV of the TF-IDF Python scripts, and
# (2) visualizes them as a series of colored word clouds, with a separate word cloud for
# each category (time periods in this case)

# Note that this chart manually defines 13 categories (one for each time period), with each
# returned as a separate word cloud. Colors are set manually, as is generation of each word
# cloud. For a differing number of categories (e.g. genres), the script must be modified so
# that the correct number of colors are defined (if desired) and word clouds generated.

# For a large number of categories (e.g. artist-specific analysis), it may not be time-
# conducive to set this up manually. In this case an iterative process to automate color
# identification or word cloud generation may be desired, however it is not implemented in
# this script.

# Finally, if a differing number of top words/scores is returned, the appropriate lines will
# need to be adjusted accordingly. These show the relevant lines set for reading a CSV
# containing the top 10 words:
# (1) for item in range(10):
# (2) value = float(row[item+10])

import csv

from wordcloud import WordCloud

import matplotlib.pyplot as plt
import random

# Define colors (same as used for R plot)
# Colors extracted from R plot with RGB to HSL Conversion at 
# https://www.rapidtables.com/convert/color/rgb-to-hsl.html
# 1950s
def color_func_1(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(5, 89.7%%, %d%%)" % random.randint(40, 80)
# 1960-1964
def color_func_2(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(37, 100%%, %d%%)" % random.randint(40, 80)
# 1965-1969
def color_func_3(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(49, 100%%, %d%%)" % random.randint(40, 80)
# 1970-1974
def color_func_4(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(71, 100%%, %d%%)" % random.randint(40, 80)
# 1975-1979
def color_func_5(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(108, 100%%, %d%%)" % random.randint(40, 80)
# 1980-1984
def color_func_6(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(155, 100%%, %d%%)" % random.randint(40, 80)
# 1985-1989
def color_func_7(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(174, 99%%, %d%%)" % random.randint(40, 80)
# 1990-1994
def color_func_8(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(189, 100%%, %d%%)" % random.randint(40, 80)
# 1995-1999
def color_func_9(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(199, 100%%, %d%%)" % random.randint(40, 80)
# 2000-2004
def color_func_10(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(236, 98.3%%, %d%%)" % random.randint(50, 90)
# 2005-2009
def color_func_11(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(282, 97.1%%, %d%%)" % random.randint(40, 80)
# 2010-2014
def color_func_12(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(311, 91.5%%, %d%%)" % random.randint(40, 80)
# 2015-2019
def color_func_13(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(332, 100%%, %d%%)" % random.randint(40, 80)

# Generate separate word clouds for each decade

with open("AllRecords_PeriodTFIDF_LyricWikia_Top10.csv",newline='') as csvfile:
    recordReader = csv.reader(csvfile, delimiter = ',')
    next(recordReader, None)
    allWordsDict = {}
    index = 1
    for row in recordReader:
        #print(row)
        period = row[0]
        #print(period)
        del row[0]
        wordsDict = {}
        for item in range(10):
            word = row[item]
            #print(word)
            value = float(row[item+10])
            #print(value)
            wordsDict[word] = value
        #print(wordsDict)
        wcloud = WordCloud().generate_from_frequencies(wordsDict)
        #colorFunc = "color_func_%s" % index
        #print(colorFunc)
        if index == 1:
            plt.imshow(wcloud.recolor(color_func=color_func_1, random_state=3),interpolation="bilinear")
        elif index == 2:
            plt.imshow(wcloud.recolor(color_func=color_func_2, random_state=3),interpolation="bilinear")
        elif index == 3:
            plt.imshow(wcloud.recolor(color_func=color_func_3, random_state=3),interpolation="bilinear")
        elif index == 4:
            plt.imshow(wcloud.recolor(color_func=color_func_4, random_state=3),interpolation="bilinear")
        elif index == 5:
            plt.imshow(wcloud.recolor(color_func=color_func_5, random_state=3),interpolation="bilinear")
        elif index == 6:
            plt.imshow(wcloud.recolor(color_func=color_func_6, random_state=3),interpolation="bilinear")
        elif index == 7:
            plt.imshow(wcloud.recolor(color_func=color_func_7, random_state=3),interpolation="bilinear")
        elif index == 8:
            plt.imshow(wcloud.recolor(color_func=color_func_8, random_state=3),interpolation="bilinear")
        elif index == 9:
            plt.imshow(wcloud.recolor(color_func=color_func_9, random_state=3),interpolation="bilinear")
        elif index == 10:
            plt.imshow(wcloud.recolor(color_func=color_func_10, random_state=3),interpolation="bilinear")
        elif index == 11:
            plt.imshow(wcloud.recolor(color_func=color_func_11, random_state=3),interpolation="bilinear")
        elif index == 12:
            plt.imshow(wcloud.recolor(color_func=color_func_12, random_state=3),interpolation="bilinear")
        elif index == 13:
            plt.imshow(wcloud.recolor(color_func=color_func_13, random_state=3),interpolation="bilinear")
        else:
            print("This is not supposed to happen.")
        plt.axis("off")
        outfile = "WC%s.png" % index
        #print(outfile)
        plt.savefig(outfile, format="png")
        plt.show()
        index = index+1