import json
import random
import time 
import requests
from bs4 import BeautifulSoup
import codecs
from tqdm import tqdm
import re 
import os 
import sys

def main(sufixo):
    # open files with already crawled links
    crawled = {}
    if os.path.isfile('../data_'+sufixo+'/reviews.json'):
        with open('../data_'+sufixo+'/reviews.json', 'r') as f:
            crawled = json.load(f)

    # dict to save all data (stars, author, data, text, title)
    data = {}

    # open links of revs 
    links = []
    with open('../data_'+sufixo+'/links_restaurants_revs.json', 'r') as f:
        links = json.load(f)

    #remove already crawled links
    s_crawled = set()
    for key in crawled.keys():
        s_crawled.add(crawled[key]['link_ref'])
    s_links = set(links)

    print('len crawled: ', len(list(s_crawled)))
    print('len links: ', len(links))
    links = list(s_links.difference(s_crawled))
    print('len links - crawled: ', len(links))

    #add existing data
    for key in crawled.keys():
        data.update({key:crawled[key]})

    # get part
    random.shuffle(links)
    #links = links[:2]
    len_links = len(links)
    processados = 0
    total = 0

    # for each link in links
    while (len(links)>0):
        total+=1
        random.shuffle(links)
        link = links[0]
        print('link:', link)
        print("processando: %i de %i"%(total, len_links))
        try:
            resp_link = requests.get(link, timeout=5)
            time.sleep(2)
            print('retrieved ...')
            #remove
            processados+=1
            soup = BeautifulSoup(resp_link.content, 'lxml')
            #lreviews = soup.findAll("div", {"class":"prw_rup prw_reviews_text_summary_hsx"})
            #lreviews = soup.findAll("div", {"class":"review-container"})
            # div class="member_info" --> autor
            # span class="ui_bubble_rating bubble_40" --> estrelas
            # div class="quote" --> titulo
            # div class="entry" --> reviewtext
            # span class="ratingDate" --> data
            lreviews = soup.findAll("div", {"class":"review-container"})
            for review in lreviews:
                soup_review = BeautifulSoup(str(review), 'lxml')
                #idreview = review.attrs.get("data-reviewid")
                idreview = review.attrs.get('data-reviewid')
                print("idrev", idreview)
                autor, estrelas, titulo, reviewtext, fecha = "", "", "", "", ""
                try:
                    autor = soup_review.find("div", {"class":"member_info"}).text 
                    estrelas = soup_review.find(attrs={'class':re.compile(r"ui_bubble_rating bubble_*")})
                    titulo = soup_review.find("div", {"class":"quote"}).text
                    reviewtext = soup_review.find("div", {"class":"entry"}).text
                    fecha = soup_review.find(attrs={'class':re.compile(r"ratingDate")}).text 
                except Exception as e:
                    print(e)
                item = {"link_ref":link,"autor":autor, "estrelas":str(estrelas), "titulo":titulo, "reviewtext":reviewtext, "fecha":fecha}
                data.update({idreview:item})
        except Exception as e:
            print(e)
            print('exception ...')

        links.remove(link)
    print('total processados:', processados)
    #save data 
    with open('../data_'+sufixo+'/reviews.json', 'w') as out:
        json.dump(data, out, indent=4)

if __name__=='__main__':
    sufixo = sys.argv[1]
    main(sufixo) 
