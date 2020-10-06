import sys
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 

def main(link):
    #link do restaurante de uma determinada cidade
    #link = 'https://www.tripadvisor.de/Restaurants-g187323-Berlin.html'
    #base = 'https://www.tripadvisor.com/'
    #link = 'https://www.tripadvisor.com/Restaurants-g60763-New_York_City_New_York.html'
    partes = link.split('/')
    if len(partes)==4 and 'https://www.tripadvisor' in '/'.join(partes[:-1]):
        print('link correcto')
        base = '/'.join(partes[:-1])
        print('base: %s'%base)
        print('link city %s'%link)
    else:
        print('el link de entrada es incorrecto')
        print('exemplo: https://www.tripadvisor.de/Restaurants-g187323-Berlin.html')
        return

    a = requests.get(link, timeout=120)
    soup = BeautifulSoup(a.content)
    #get the pagination
    pages = soup.findAll("div", {"class":"pageNumbers"})
    s_page = BeautifulSoup(str(pages))
    nums = s_page.findAll('a')
    #get the last pagination number and link
    last_page = int(nums[-1].text)
    last_page_index = nums[-1]["href"]

    print('Pagination Info')
    print('# de paginas: %d'%(last_page))
    print('ultima pagina: %s'%(last_page_index))

    #create the list of links to access  the restaurants
    pages_link = []
    for k in range(last_page):
        ref = 30*k
        #toad = 'https://www.tripadvisor.de/RestaurantSearch?Action=PAGE&geo=187323&ajax=1&itags=10591&sortOrder=popularity&o=a'+str(ref)+'&availSearchEnabled=false'
        toad = base+'/RestaurantSearch?Action=PAGE&geo=188590&ajax=1&itags=10591&sortOrder=relevance&o=a' + str(ref) + '&availSearchEnabled=true&eaterydate=2019_04_23&date=2019-04-24&time=20%3A00%3A00&people=2'
        pages_link.append(toad)

    print(pages_link[:2])

    # para cada pagina
    links_restaurants = []
    for url in tqdm(pages_link):
        page = requests.get(url, timeout=120)
        bs_page = BeautifulSoup(page.content)
        # lista de restaurantes en la pagina actual
        restaurants = bs_page.findAll("div",{"class":"_1llCuDZj"})
        # recuperar el link de cada restaurante
        for restaurant in restaurants:
            # en la estructura actual, el link aparece en la primera posición
            ref = restaurant.findAll('a')[0].get('href')
            print(ref)
            links_restaurants.append(base+ref)

    import json
    with open('../data/links_restaurants.json', 'w') as out:
        json.dump(links_restaurants, out)

if __name__=='__main__':
    link_city = sys.argv[1]
    main(link_city) 
