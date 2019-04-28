#This code is desined to take the output from the LDA topic analysis and apply the NRC sentiment and emotion lexicon to the words in each topic.
#After reading in the csv file, punctuation and non-alpha-numeric characters are removed
#The remaining words are then fed into the get_nrc_sentiment function from the suyzhet library, which returns a dictionary of word totals for each emotion/sentiment
#The remaining code curates the data in a form suitable for export to a csv file
#The output of the csv file has the following data structure: the rows correspond to topics and the columns correspond to emotion/sentiment. The values stored are the word counts for each emotion/sentiment per topic.



library(tm)
library(ggplot2)
library(syuzhet)

f <- file("C:/Users/nippebr/Desktop/DAEN 690/NRC Analysis/topic_keywords_20.csv", "r")
#f <- file("C:/Users/nippebr/Desktop/DAEN 690/NRC Analysis/topic_keywords_30.csv", "r")
lyrics <- readLines(f)
lyrics <- gsub(",", " ", lyrics)
lyrics <- gsub('[[:punct:]]+', '', lyrics)
lyrics <- gsub("([[:alpha:]])\1+", "", lyrics)

row <- c()
anger <- c()
anticipation <- c()
disgust <- c()
fear <- c()
joy <- c()
sadness <- c()
surprise <- c()
trust <- c()
negative <- c()
positive <- c()
for (i in 1:length(lyrics)){
  row[i] <- paste("Topic", toString(i), sep = " ")
  ty_sentiment <- get_nrc_sentiment((lyrics[i]))
  anger[i] <- ty_sentiment$anger
  anticipation[i] <- ty_sentiment$anticipation
  disgust[i] <- ty_sentiment$disgust
  fear[i] <- ty_sentiment$fear
  joy[i] <- ty_sentiment$joy
  sadness[i] <- ty_sentiment$sadness
  surprise[i] <- ty_sentiment$surprise
  trust[i] <- ty_sentiment$trust
  negative[i] <- ty_sentiment$negative
  positive[i] <- ty_sentiment$positive
}

close(f)
rm(f, i, lyrics, ty_sentiment)

df <- data.frame(row, anger,anticipation,disgust,fear,joy,sadness,surprise,trust,negative,positive)
names(df) <- c("Topic","Anger","Anticipation","Disgust","Fear","Joy","Sadness","Surprise","Trust","Negative","Positive")

write.csv(df, file = "Sentiment_20_Topics.csv", row.names=FALSE)
#write.csv(df, file = "Sentiment_30_Topics.csv", row.names=FALSE)

rm(df, anger, anticipation, disgust, fear, joy, negative, positive, sadness, surprise, trust, row)