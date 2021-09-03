import sys
import requests
#from bs4 impor BeautifulSoup
from utils.utils import *
import tqdm
import random

def main(sufixo):
    # open links of pagination
    links_pagination = []
    with open('../data_'+sufixo+'/links_pagination.json', 'r') as f:
        links_pagination = json.load(f)

    # get link base
    parts = links_pagination[0].split('/')
    base = '/'.join(parts[:-1])
    print('base:', base)

    # open files with already crawled pagination and restaurant links
    crawled = {}
    if os.path.isfile('../data_'+sufixo+'/links_restaurants.json'):
        with open('../data_'+sufixo+'/links_restaurants.json', 'r') as f:
            crawled = json.load(f)
    # 
    links_pagination_crawled = crawled.keys()

    # printar info
    s_links_pagination = set(links_pagination)
    s_links_pagination_crawled = set(links_pagination_crawled)
    s_links_pagination_faltante = s_links_pagination.difference(s_links_pagination_crawled)
    print('total pagination:', len(s_links_pagination))
    print('total pagination crawled:', len(s_links_pagination_crawled))
    print('total pagination faltantes:', len(s_links_pagination_faltante))

    pages = list(s_links_pagination_faltante)
    # recuperar links de los restaurantes por cada link de pagination
    #for page in pages:
    len_pages = len(pages)
    total = 0
    processados = 0
    while (len(pages)>0):
        total +=1
        random.shuffle(pages)
        page = pages[0]
        #get link pagination to retrieve links of restaurants
        print('processando: ', page)
        print('%i de %i'%(total, len_pages))
        resp_requests, erro = get_link(page, 5)
        if resp_requests is not None:
            restaurants = exactmatch_items(resp_requests, "div", "class", "_1llCuDZj")
            print('retrieved')
            links_restaurants = []
            for restaurant in restaurants:
                # en la estructura actual, el link aparece en la primera posición
                ref = restaurant.findAll('a')[0].get('href')
                print(ref)
                links_restaurants.append(base+ref)
            crawled.update({page:{'restaurants':links_restaurants}})
        else:
            print('aqui')
            print(erro)
        pages.remove(page)
    write_json('../data_'+sufixo+'/links_restaurants.json', crawled)

if __name__ == '__main__':
    sufixo = sys.argv[1]
    main(sufixo)
