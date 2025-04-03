import time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

main = 'https://www.azlyrics.com'

def run_scrape(url):
    source = requests.get(url)
    time.sleep(5)
    html = BeautifulSoup(source.text, "html.parser")

    artist_box = html.find('div', class_ = 'col-xs-12 col-lg-8 text-center')
    artist_name = artist_box.h1.strong.text.replace(' Lyrics', '')
    print(f'Artist Name: {artist_name}')
    
    songs = html.find_all('div', class_ = 'listalbum-item')
    song_names = []
    href = []
    lyrics = []
    release_types = []
    types_name = []

    for detail in songs:
        name = detail.a.text
        url_to_lyric = detail.a['href']
        song_names.append(name)
        href.append(f'{main}{url_to_lyric}')


    count = 0
    for link in href:
        sub_source = requests.get(link)
        sub_html = BeautifulSoup(sub_source.text, "html.parser")
        time.sleep(5)

        
        types = sub_html.find('div', class_ = 'songinalbum_title')
        if types != None:
            full_type_text = types.text
            typ = full_type_text.split(':')
            release_types.append(typ[0])

            type_name = types.b.text
            types_name.append(type_name)

        else:
            release_types.append('Not specified')
            types_name.append('Other songs')
        
        
        lyrs_br = sub_html.find_all('div', class_ = None)
        lyrs = lyrs_br[2].text
        sent = lyrs.replace('[Romanized:]', '')
        lyrics.append(sent.replace('\n', ''))
        

        count += 1
        print(f'[{count}]: {song_names[count-1]}')


    df = pd.DataFrame({'release type' : release_types,
                    'album name' : types_name,
                    'name' : song_names,
                    'lyric' : lyrics,
                    'link' : href,
                    })


    df.to_csv(f'{artist_name}.csv')


if __name__ == "__main__":
    run_scrape('https://www.azlyrics.com/k/keshi.html')
    #scrap('https://www.azlyrics.com/j/joji.html')
    #scrap('https://www.azlyrics.com/j/jvke.html')
