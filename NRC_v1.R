#This code is desined to take one of the cleaned lyrics datasets and apply the NRC sentiment and emotion lexicon to the words in each song.
#After reading in the csv file, punctuation and non-alpha-numeric characters are removed
#The remaining words are then fed into the get_nrc_sentiment function from the suyzhet library, which returns a dictionary of word totals for each emotion/sentiment
#The remaining code curates the data in a form suitable for export to a csv file
#The output of the csv file has the following data structure: the rows correspond to songs and the columns correspond to emotion/sentiment. The values stored are the word counts for each emotion/sentiment per song.


library(tm)
library(ggplot2)
library(syuzhet)

#lyrics <- read.csv(file="C:/Users/nippebr/Desktop/DAEN 690/NRC Analysis/Data.csv", header=TRUE, sep=",") # LyricsWikia
lyrics <- read.csv(file="C:/Users/nippebr/Desktop/DAEN 690/NRC Analysis/Data_Cleaned_Dupes_Removed.csv", header=TRUE, sep=",") #MetroLyrics

# lyrics <- lyrics[lyrics$Year > 1900 & lyrics$Year < 2020,]
# lyrics1900 <- lyrics[lyrics$Year >= 1900 & lyrics$Year < 1910,]
# lyrics1910 <- lyrics[lyrics$Year >= 1910 & lyrics$Year < 1920,]
# lyrics1920 <- lyrics[lyrics$Year >= 1920 & lyrics$Year < 1930,]
# lyrics1930 <- lyrics[lyrics$Year >= 1930 & lyrics$Year < 1940,]
# lyrics1940 <- lyrics[lyrics$Year >= 1940 & lyrics$Year < 1950,]
# lyrics1950 <- lyrics[lyrics$Year >= 1950 & lyrics$Year < 1960,]
# lyrics1960 <- lyrics[lyrics$Year >= 1960 & lyrics$Year < 1970,]
# lyrics1970 <- lyrics[lyrics$Year >= 1970 & lyrics$Year < 1980,]
# lyrics1980 <- lyrics[lyrics$Year >= 1980 & lyrics$Year < 1990,]
# lyrics1990 <- lyrics[lyrics$Year >= 1990 & lyrics$Year < 2000,]
# lyrics2000 <- lyrics[lyrics$Year >= 2000 & lyrics$Year < 2010,]
# lyrics2010 <- lyrics[lyrics$Year >= 2010 & lyrics$Year < 2020,]

Lyrics <- lyrics$Lyrics
Lyrics <- gsub('[[:punct:]]+', '', Lyrics)
Lyrics <- gsub("([[:alpha:]])\1+", "", Lyrics)

ty_sentiment <- get_nrc_sentiment((Lyrics))
sentimentscores <- data.frame(colSums(ty_sentiment[,]))

lyrics_new <- within(lyrics, rm(Band.Popularity, Lyrics, Year, Song.Popularity))
lyrics_new$anger <- ty_sentiment$anger
lyrics_new$anticipation <- ty_sentiment$anticipation
lyrics_new$disgust <- ty_sentiment$disgust
lyrics_new$fear <- ty_sentiment$fear
lyrics_new$joy <- ty_sentiment$joy
lyrics_new$sadness <- ty_sentiment$sadness
lyrics_new$surprise <- ty_sentiment$surprise
lyrics_new$trust <- ty_sentiment$trust
lyrics_new$negative <- ty_sentiment$negative
lyrics_new$positive <- ty_sentiment$positive

write.csv(lyrics_new, file = "Sentiment_All_MetroLyrics.csv", row.names=FALSE)

# names(sentimentscores) <- "Score"
# sentimentscores <- cbind("sentiment"=rownames(sentimentscores),sentimentscores)
# rownames(sentimentscores) <- NULL
# 
# ggplot(data=sentimentscores,aes(x=sentiment,y=Score))+
#   geom_bar(aes(fill=sentiment),stat = "identity")+
#   theme(legend.position="none")+
#   xlab("Sentiments")+ylab("Scores")+
#   ggtitle("Total sentiment based on scores")+
#   theme_minimal()