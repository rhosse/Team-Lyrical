# -*- coding: utf-8 -*-

# LyricsWikia Web Crawlwer
#
# Brandon Nipper

from bs4 import BeautifulSoup
import requests, time
import pandas as pd

start = time.time()

letter = 'Z'

rootURL = 'http://lyrics.wikia.com/wiki/Category:Artists_'+letter
outFile = letter+'_LyricWikia.csv'

print("Building Arist URL list: %f s" % (time.time()-start))
urlRoot = "http://lyrics.wikia.com"
artists = []
artistURLs = []
page_good = False
pageNum = 1
numTries = 0
while not page_good:
    try:
        page_response = requests.get(rootURL, timeout=5)
        page_good = True
    except:
        print("Page timed out. Waiting 2 s before trying again.")
        time.sleep(2)
        if numTries > 5:
            break
        else:
            numTries += 1

page_content = BeautifulSoup(page_response.content, "html.parser")

print("Getting Artists from Page %d: %f s" % (pageNum,time.time()-start))

lastURL = ''
nextURL = ''
uls = page_content.find_all("ul")
ulFlag = 0
ulList = []
for i in range(1, len(uls)):
    if uls[i].get("class") == ['category-page__members-for-char']:
        ulFlag += 1
        ulList.append(uls[i])
        
lis = ulList[-1].find_all("li")
for li in lis:
    aas = li.find_all("a")
    for a in aas:
        artist = a.get("title")
        artists.append(artist)
        link = a.get("href")
        artistURLs.append(urlRoot+link)
            
isLastPage = True
divs = page_content.find_all("div")
for i in range(1, len(divs)):
    if divs[i].get("class") == ['category-page__pagination']:
        aas = divs[i].find_all("a")
        for a in aas:
            if a.text.strip() == "Next":
                nextURL = a.get("href")
            elif a.text.strip() == "Last":
                lastURL = a.get("href")
                isLastPage = False
                
while not isLastPage:
    pageNum += 1
    print("Getting Artists from Page %d: %f s" % (pageNum,time.time()-start))
    isLastPage = True
    
    page_good = False
    numTries = 0
    while not page_good:
        try:
            page_response = requests.get(nextURL, timeout=5)
            page_good = True
        except:
            print("Page timed out. Waiting 2 s before trying again.")
            time.sleep(2)
            if numTries > 5:
                break
            else:
                numTries += 1
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    uls = page_content.find_all("ul")
    ulFlag = 0
    for i in range(1, len(uls)):
        if uls[i].get("class") == ['category-page__members-for-char']:
            ulFlag += 1
            if ulFlag >= 1:
                lis = uls[i].find_all("li")
                for li in lis:
                    aas = li.find_all("a")
                    for a in aas:
                        artist = a.get("title")
                        artists.append(artist)
                        link = a.get("href")
                        artistURLs.append(urlRoot+link)
                        
    divs = page_content.find_all("div")
    for i in range(1, len(divs)):
        if divs[i].get("class") == ['category-page__pagination']:
            aas = divs[i].find_all("a")
            for a in aas:
                if a.text.strip() == "Next":
                    nextURL = a.get("href")
                elif a.text.strip() == "Last":
                    lastURL = a.get("href")
                    isLastPage = False
                    
titles = []
for i in range(len(artists)):
    print("Getting Song Info for Artist %d of %d: %f s" % (i+1,len(artists),time.time()-start))
    url = artistURLs[i]
    artist = artists[i]
    page_good = False
    numTries = 0
    while not page_good:
        try:
            page_response = requests.get(url, timeout=5)
            page_good = True
        except:
            print("Page timed out. Waiting 2 s before trying again.")
            time.sleep(2)
            if numTries > 5:
                break
            else:
                numTries += 1
    page_content = BeautifulSoup(page_response.content, "html.parser")
    
    h2s = page_content.find_all("h2")
    years = []
    for h2 in h2s:
        aas = h2.find_all("a")
        if len(aas) > 1:
            title = aas[0].get("title")
            if title != None:
                year = title[title.find('(') + 1 : title.find(')')]
            else:
                year = float('nan')
            years.append(year)
            
    ols = page_content.find_all("ol")
    for j in range(1,len(years)+1):
        try:
            aas = ols[j].find_all("a")
            for a in aas:
                title = a.get("title")
                title = title[len(artist)+1:]
                link = a.get("href")
                if link != None:
                    link = urlRoot + link
                    page_good = False
                    numTries = 0
                    while not page_good:
                        try:
                            page_response = requests.get(link, timeout=5)
                            page_good = True
                        except:
                            print("Page timed out. Waiting 2 s before trying again.")
                            time.sleep(2)
                            if numTries > 5:
                                break
                            else:
                                numTries += 1
                    page_content = BeautifulSoup(page_response.content, "html.parser")
    #                for linebreak in page_content.find_all('br'):
    #                    linebreak.extract()
                    str(page_content).replace("<br/>", " ")
                    divs = page_content.find_all("div")
                    lyrics = ''
                    for div in divs:
                        if div.get("class") == ['lyricbox']:
                            lyrics = str(div).replace("<br/>", " ")[22:-38]
                    
                else:
                    link = ''
                    lyrics = ''
                titles.append((artist,years[j-1],title, lyrics))
        except:
            print("Bad data. Ignoring page." )

dataHeader = ['Artist','Year','Song','Lyrics']
print("Writing to CSV: %f s" % (time.time()-start))
df = pd.DataFrame(titles, columns=dataHeader)
df.to_csv(outFile, index=False)
        
print("Script Completed after %f s" % (time.time()-start))

del start, rootURL, outFile, page_good, page_response, i, lis, ulFlag, uls, aas, a, divs, isLastPage, lastURL, nextURL, pageNum, urlRoot, url, h2s, year, j, ols, years, artist, artistURLs, artists, link, lyrics, title, dataHeader, df, letter, ulList