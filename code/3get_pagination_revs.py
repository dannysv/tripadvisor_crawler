import json
import random
import requests
from tqdm import tqdm
import sys
from utils.utils import *


#jsonin {linkrestpagination:{"restaurant":[links_restaurants]}}
#jsonout {linkrestaurant:{"pagination":[links_restaurant_revs]}}
def main(sufixo, limite):
    jsonin = '../data_'+sufixo+'/links_restaurants.json'
    jsonout = '../data_'+sufixo+'/links_pagination_revs.json'
    # open the list of all restaurants
    dictin, erro = read_json(jsonin)
    linkrestaurants = []
    if dictin is not None:
        for restpage in dictin.keys():
            linkrestaurants += dictin[restpage]['restaurants']
    linkrestaurants = linkrestaurants[:limite]
    # get link base
    parts = linkrestaurants[0].split('/')
    base = '/'.join(parts[:-1])

    print('base:', base)

    # open jsonout to know which part is already retrieved
    dictout, erro = read_json(jsonout)
    linkrestaurants_crawled = []
    if dictout is not None:
        linkrestaurants_crawled = dictout.keys()
    else:
        dictout = {}
    
    # print info
    s_linkrestaurants = set(linkrestaurants)
    s_linkrestaurants_crawled = set(linkrestaurants_crawled)
    s_linkrestaurants_faltante = s_linkrestaurants.difference(linkrestaurants_crawled)
    print('Total : ', len(list(s_linkrestaurants)))
    print('Ya processados: ', len(list(s_linkrestaurants_crawled)))
    print('Faltantes: ', len(list(s_linkrestaurants_faltante)))

    # processar os links que estão faltando
    linkrestaurants_faltante = list(s_linkrestaurants_faltante)
    len_links = len(linkrestaurants_faltante)
    total = 0
    processados = 0
    while (len(linkrestaurants_faltante)>0):
        total+=1
        print("processando %i de %i"%(total, len_links))
        #shuffle the list of links
        random.shuffle(linkrestaurants_faltante)
        # get the first link
        link = linkrestaurants_faltante[0]
        print(link)
        resp_link, error = get_link(link, 5)
        if resp_link is not None:
            item = exactmatch_item(resp_link, 'span', 'class', '_3Wub8auF')
            #print('aqui', item)
            number = 0
            try:
                print(item.text)
                number = int(item.text.split(' ')[0].replace(',', ''))
            except Exception as e:
                print(e)
            # obtener pagination 
            # https://www.tripadvisor.com/Restaurant_Review-g34439-d7278103-Reviews-or10-CVI_CHE_105-Miami_Beach_Florida.html
            lista = []     
            for i in range(0, number, 10):
                change = '-Reviews-or'+str(i)+'-'
                linkpagerev = link.replace('-Reviews-', change)
                print(linkpagerev)
                lista.append(linkpagerev)
            # crear item y atualizar arquivo de saida
            item = {"pagination":lista}
            dictout.update({link:item})
        else:
            print(error)
        linkrestaurants_faltante.remove(link)
    #write dictout
    write_json(jsonout, dictout)

if __name__ =='__main__':
    sufixo = sys.argv[1]
    try:
        limite = sys.argv[2]
        limite = int(limite)
        main(sufixo, limite)
    except Exception as e:
        print(e)
        print('argumento 2 invalido')
