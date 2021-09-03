import sys
import requests
#from bs4 impor BeautifulSoup
from utils.utils import *
import tqdm

def main(link, sufixo, number):
    # link of a given restaurant
    # example --> https://www.tripadvisor.com.br/Restaurants-g303631-Sao_Paulo_State_of_Sao_Paulo.html
    parts = link.split('/')
    #check the correctness of the link
    if len(parts)==4 and 'https://www.tripadvisor.co' in '/'.join(parts[:-1]):
        print('link correcto')
        base = '/'.join(parts[:-1])
        print('base: %s' %base)
        print('link of the city: %s'%link)
        #get the code of the restaurant 
        #https://www.tripadvisor.com.br/Restaurants-g303631-Sao_Paulo_State_of_Sao_Paulo.html
        #https://www.tripadvisor.com.br/RestaurantSearch-g303631-oa30-Sao_Paulo_State_of_Sao_Paulo.html
        restaurant = parts[-1]
        partshyphen = restaurant.split('-')
        if len(partshyphen) == 3:
            links_pagination = []
            # recuperar links de los restaurantes por cada link de pagination
            for i in tqdm.tqdm(range(number)):
                linkpage = base + '/' + partshyphen[0]+'-'+partshyphen[1]+'-oa'+str(i*30)+'-'+partshyphen[-1]
                links_pagination.append(linkpage)
            write_json('../data_'+sufixo+'/links_pagination.json', links_pagination)
        else:
            print('error en el link')
    else:
        print('formato de link incorrecto')
        print('exemplo: https://www.tripadvisor.de/Restaurants-g187323-Berlin.html')

if __name__ == '__main__':
    link = sys.argv[1]
    sufixo = sys.argv[2]
    numberpages = sys.argv[3]
    try:
        numberpages = int(numberpages)
        if os.path.isdir('../data_'+sufixo):
            print('ya existe sufixo, cambiar')
        else:
            os.mkdir('../data_'+sufixo)
            main(link, sufixo, numberpages)
    except Exception as e:
        print(e)
        print('invalid number of pages')
