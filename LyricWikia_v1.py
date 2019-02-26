# -*- coding: utf-8 -*-

# LyricsWikia Data Acquisition
#
# Brandon Nipper

import pandas as pd
import pylyrics3, time, re

def generateSongList(songdict):
    
    songs = []
    years = []
    lyrics = []
    
    if len(songdict) == 0:
        return songs, years
    
    for album_year in songdict:
        temp = str(album_year)
        year = temp[temp.find('(') + 1 : temp.find(')')]
        for song in songdict[album_year]:
            songs.append(song.lower())
            years.append(year)
            lyric = songdict[album_year][song]
            lyric = re.sub('[\n?()\"\'-,.#$%~@^&*_+={};:<>]', '', lyric)
            lyrics.append(lyric)
    return songs, years, lyrics

start = time.time()

inFile = 'Y(3).csv'
outFile = inFile[:-6]+'4).csv'

data = pd.read_csv(inFile)
artists = data['Artist'].unique()

newData = pd.DataFrame(columns=['Artist','Genre','Band Popularity','Song','Year','Song Popularity','Lyrics','pyYear','pyLyrics'])

numMatched = 0
for idx, artist in enumerate(artists):
#    if idx > 50:
#        break
    print("Getting data for %s, artist %d of %d: %f s" % (artist, idx, len(artists), time.time()-start))
    artistSongs = data.loc[data['Artist'] == artist]
    artist_clean = artist.strip().lower().replace(',','')
    
    try:
        songdict = pylyrics3.get_artist_lyrics(artist_clean, albums=True)
        if songdict != None:
            numMatched += 1
            pyArtistSongs, pyArtistYears, lyrics = generateSongList(songdict)
            
            pyYear = []
            pyLyrics = []
            for idx, song in enumerate(artistSongs['Song']):
                songLower = re.sub('[\n?()\"\'-,.#$%~@^&*_+={};:<>]', '', song)
                songLower = songLower.lower()
                
                if songLower in pyArtistSongs:
                    pyYear.append(pyArtistYears[pyArtistSongs.index(songLower)])
                    pyLyrics.append(lyrics[pyArtistSongs.index(songLower)])
                else:
                    pyYear.append('')
                    pyLyrics.append('')
                
                artistSongs['Song'] = artistSongs['Song'].replace(song, songLower)
                
#            artistSongs['pyYear'] = pyYear
#            artistSongs['pyLyrics'] = pyLyrics
        else:
            print("Couldn't retrieve data for %s" % (artist))
            pyYear = []
            pyLyrics = []
            for idx, song in enumerate(artistSongs['Song']):
                pyYear.append('')
                pyLyrics.append('')
#            artistSongs['pyYear'] = pyYear
#            artistSongs['pyLyrics'] = pyLyrics
    except:
        print("Couldn't retrieve data for %s" % (artist))
        pyYear = []
        pyLyrics = []
        for idx, song in enumerate(artistSongs['Song']):
            pyYear.append('')
            pyLyrics.append('')
            
    artistSongs['pyYear'] = pyYear
    artistSongs['pyLyrics'] = pyLyrics
    
    newData = pd.concat([newData, artistSongs])
    
newData.to_csv(outFile, index=False)

print(time.time()-start)

del data, artist_clean, artists, start, artist, artistSongs, idx, lyrics, newData, numMatched, pyArtistSongs, pyArtistYears, pyLyrics, pyYear, song, songLower, songdict, inFile, outFile