# MetroLyrics web scraper
#
# Brandon Nipper

from bs4 import BeautifulSoup
import requests, time
import pandas as pd

def getData(url, urls):
    page_good = False
    while not page_good:
        try:
            page_response = requests.get(url, timeout=5)
            page_good = True
        except:
            print("Page timed out. Waiting 2 s before trying again.")
            time.sleep(2)
    
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    trs = page_content.find_all("tr")
    bandData = []
    for i in range(1,len(trs)):
        tds = trs[i].find_all("td")
        
        metas = trs[i].find_all("meta")
        group = metas[1].get("content").replace(',', '')
        genre = tds[1].text    
        styles = tds[2].find_all("span")
        band_popularity = float(styles[1].get("style")[6:][:-2])
    
        band_url = metas[0].get("content")
        
        bandData.append((group, genre, band_popularity, band_url))
        
    ps = page_content.find_all("p")
    #is_last_page = True
    for p in ps:
        if p.get("class") != ['pagination']:
            continue
        else:
            #is_last_page = False
            spans = p.find_all("span")
            for span in spans:
                if span.get("class") != ['pages']:
                    continue
                else:
                    aas = span.find_all("a")
                    for a in aas:
                        link = a.get("href")
                        if link not in urls:
                            urls.append(link)
#                            bandData = bandData + getData(link, urls, numPag, noPag)
                            bandData = bandData + getData(link, urls)
        
    return bandData       

def getSongData(band):
    url = band[3]
    
    urls = []
    urls = urls + getSongURLs(url, urls)
    
    songs = []
    for url in urls:
        songs = songs + getSongs(url, band)
    
    
    return songs

def getSongs(url, band):
    page_good = False
    while not page_good:
        try:
            page_response = requests.get(url, timeout=5)
            page_good = True
        except:
            print("Page timed out. Waiting 2 s before trying again.")
            time.sleep(2)
            
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    songList = []
    divs = page_content.find_all("div")
    for div in divs:
        if div.get("class") != ['switchable', 'lyrics', 'clearfix']:
            continue
        else:
            try:
                tBody = div.find_all("tbody")
                trs = tBody[0].find_all("tr")
                for tr in trs:
                    tds = tr.find_all("td")
                    song = tds[1].find_all("a")[0].text.strip()
                    link = tds[1].find_all("a")[0].get("href")
                    year = tds[2].text
                    styles = tds[3].find_all("span")
                    song_popularity = float(styles[1].get("style")[6:][:-2])
                    
                    songList.append((band[0],band[1],band[2],song,year,song_popularity,link))
            except:
                return []                
    return songList

def getSongURLs(url, urls):
    page_good = False
    while not page_good:
        try:
            page_response = requests.get(url, timeout=5)
            page_good = True
        except:
            print("Page timed out. Waiting 2 s before trying again.")
            time.sleep(2)
            
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    ps = page_content.find_all("p")
    has_pagination = False
    for p in ps:
        if p.get("class") != ['pagination']:
            continue
        else:
            has_pagination = True
            page = p
            
    if has_pagination:
        spans = page.find_all("span")
        for span in spans:
            if span.get("class") != ['pages']:
                continue
            else:
                aas = span.find_all("a")
                for a in aas:
                    link = a.get("href")
                    if link not in urls:
                        urls = urls + [link]
                        urls = urls + getSongURLs(link, urls)
                    else:
                        return []
        return urls
    else:
        return [url]
    
def getLyrics(song):
    page_good = False
    while not page_good:
        try:
            page_response = requests.get(song[6], timeout=5)
            page_good = True
        except:
            print("Page timed out. Waiting 2 s before trying again.")
            time.sleep(2)
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    lyrics = []
    ps = page_content.find_all("p")
    for p in ps:
        if p.get("class") != ['verse']:
            continue
        else:
            lyrics.append(p.text.replace('\n',' ').replace('.', '').replace('?','').replace('!','').replace(':','').replace(';','').replace(',','').lower())
    songLyrics = " ".join(lyrics)
    
    return [(song[0],song[1],song[2],song[3],song[4],song[5],songLyrics)]
    
    
    
start = time.time()

#urls = ["http://www.metrolyrics.com/artists-a-1.html"]
#outFile = 'A.csv'

urls = ["http://www.metrolyrics.com/artists-b-1.html"]
outFile = 'B.csv'

#urls = ["http://www.metrolyrics.com/artists-c-1.html"]
#outFile = 'C.csv'
#
#urls = ["http://www.metrolyrics.com/artists-d-1.html"]
#outFile = 'D.csv'
#
#urls = ["http://www.metrolyrics.com/artists-e-1.html"]
#outFile = 'E.csv'
#
#urls = ["http://www.metrolyrics.com/artists-f-1.html"]
#outFile = 'F.csv'
#
#urls = ["http://www.metrolyrics.com/artists-g-1.html"]
#outFile = 'G.csv'
#
#urls = ["http://www.metrolyrics.com/artists-h-1.html"]
#outFile = 'H.csv'
#
#urls = ["http://www.metrolyrics.com/artists-i-1.html"]
#outFile = 'I.csv'
#
#urls = ["http://www.metrolyrics.com/artists-j-1.html"]
#outFile = 'J.csv'
#
#urls = ["http://www.metrolyrics.com/artists-k-1.html"]
#outFile = 'K.csv'
#
#urls = ["http://www.metrolyrics.com/artists-l-1.html"]
#outFile = 'L.csv'
#
#urls = ["http://www.metrolyrics.com/artists-m-1.html"]
#outFile = 'M.csv'
#
#urls = ["http://www.metrolyrics.com/artists-n-1.html"]
#outFile = 'N.csv'
#
#urls = ["http://www.metrolyrics.com/artists-o-1.html"]
#outFile = 'O.csv'
#
#urls = ["http://www.metrolyrics.com/artists-p-1.html"]
#outFile = 'P.csv'
#
#urls = ["http://www.metrolyrics.com/artists-q-1.html"]
#outFile = 'Q.csv'
#
#urls = ["http://www.metrolyrics.com/artists-r-1.html"]
#outFile = 'R.csv'
#
#urls = ["http://www.metrolyrics.com/artists-s-1.html"]
#outFile = 'S.csv'
#
#urls = ["http://www.metrolyrics.com/artists-t-1.html"]
#outFile = 'T.csv'
#
#urls = ["http://www.metrolyrics.com/artists-u-1.html"]
#outFile = 'U.csv'
#
#urls = ["http://www.metrolyrics.com/artists-v-1.html"]
#outFile = 'V.csv'
#
#urls = ["http://www.metrolyrics.com/artists-w-1.html"]
#outFile = 'W.csv'
#
#urls = ["http://www.metrolyrics.com/artists-x-1.html"]
#outFile = 'X.csv'
#
#urls = ["http://www.metrolyrics.com/artists-y-1.html"]
#outFile = 'Y.csv'
#
#urls = ["http://www.metrolyrics.com/artists-z-1.html"]
#outFile = 'Z.csv'

print("Gathering Artist Data: %f s" % (time.time()-start))
artistData = []
for url in urls:
#    data, numPag, noPag = data + getData(url, urls, 0, 0)
    artistData = artistData + getData(url, urls,)
print("Finished gathering artist data: %f s" % (time.time()-start))
del url, urls

print("Starting to gather song data: %f s" % (time.time()-start))
songData = []
for idx, band in enumerate(artistData):
    print("Getting band %d of %d: %f s" % (idx, len(artistData), time.time()-start))
    songData = songData + getSongData(band)
    
print("Finished gathering song data: %f s" % (time.time()-start))

del idx, band

print("Starting to gather lyrics data: %f s" % (time.time()-start))
lyricsData = []
for idx, song in enumerate(songData):
    print("Getting song %d of %d: %f s" % (idx, len(songData), time.time()-start))
    lyricsData = lyricsData + getLyrics(song)

print("Finished gathering song data: %f s" % (time.time()-start))    
del idx, song

dataHeader = ['Artist','Genre','Band Popularity','Song','Year','Song Popularity','Lyrics']

print("Writing to CSV: %f s" % (time.time()-start))
df = pd.DataFrame(lyricsData, columns=dataHeader)
df.to_csv(outFile, index=False)
print("Finished writing to CSV: %f s" % (time.time()-start))

del artistData, dataHeader, lyricsData, songData, start, outFile