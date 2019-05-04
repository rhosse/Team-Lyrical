# R Code to visualize Top TF-IDF Terms by 5-year period

# This script: 
# (1) ingests the output CSV of the TF-IDF Python scripts, and 
# (2) visualizes them as (first) individual bar charts for each category (e.g. genre, time period, etc.) as well 
# as a combined bar chart merging all results into a single plot.

# Note that this chart is currently configured to return the top 10 words and scores, if a different number of
# words and scores are returned then the "Break out" and "Combined" actions (lines 21-32 and 34-45 respectively)
# will need to be either expanded or reduced.

library(ggplot2)
library(dplyr)

# Set working directory to where the output file is located
setwd("WORKING DIRECTORY")

# Read CSV file
wordsAndScores = read.csv("AllRecords_PeriodTFIDF_LyricWikia_Top10.csv")

#wordsAndScores

# Break out matrix into separate matrices for each of the top 10 words by time period with 3 
# contents: (1) Time Period, (2) Word, and (3) Score
word1 = wordsAndScores[,c(1,2,12)]
word2 = wordsAndScores[,c(1,3,13)]
word3 = wordsAndScores[,c(1,4,14)]
word4 = wordsAndScores[,c(1,5,15)]
word5 = wordsAndScores[,c(1,6,16)]
word6 = wordsAndScores[,c(1,7,17)]
word7 = wordsAndScores[,c(1,8,18)]
word8 = wordsAndScores[,c(1,9,19)]
word9 = wordsAndScores[,c(1,10,20)]
word10 = wordsAndScores[,c(1,11,21)]

# Combine into one three-column matrix
colNames = c("Period", "Word", "Score")
names(word1) <- colNames
names(word2) <- colNames
names(word3) <- colNames
names(word4) <- colNames
names(word5) <- colNames
names(word6) <- colNames
names(word7) <- colNames
names(word8) <- colNames
names(word9) <- colNames
names(word10) <- colNames

wordsFinal = rbind(word1, word2, word3, word4, word5, word6, word7, word8, word9, word10)

wordsFinal %>%
  arrange(desc(Score)) %>%
  mutate(Word = factor(Word, levels = rev(unique(Word))))

# Provide individual bar charts for top TF-IDF words for each 5-year period (plus the 1950s)
windows(width=15,height=10)
outputPlot <-
  (ggplot(wordsFinal, aes(x=reorder(Word, Score), y=Score, fill=Period)) +
  geom_col(show.legend = FALSE) +
  labs(title = "Top 10 TF-IDF Scores (most relevant words) by 5-Year Period", x=NULL, y = "TF-IDF") +
  theme(text = element_text(size=10)) +
  theme(plot.title = element_text(size=20, hjust = 0.5)) +
  facet_wrap(~Period, ncol=4, scales="free") +
  coord_flip())
outputPlot

#ggsave(filename="plot1.jpg", plot=outputPlot)

# Provide a combined bar chart merging all TF-IDF results into a single plot
windows(width=13,height=15) # switch to width 15, height 10 for vertical bar chart
outputPlot2 <-
  (ggplot(wordsFinal, aes(x=reorder(Word, Score), y=Score, fill=Period)) + # Put "-" in front of "Score" in x for vertical
     geom_col(show.legend = TRUE) +
     labs(title = "Combined View of Highest TF-IDF Scores", x=NULL, y = "TF-IDF") +
     #theme(text = element_text(size=10)))
     theme(axis.text.x = element_text(size=8, angle=90, hjust=1)) +
     theme(plot.title = element_text(size=20, hjust = 0.5)) +
     coord_flip()) # comment out this last line for a vertical bar chart
outputPlot2

ggsave(filename="plot2a.jpg", plot=outputPlot2)
