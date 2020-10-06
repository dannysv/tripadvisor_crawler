import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm 

links = []
with open('../data/links_restaurants.json', 'r') as f:
    links = json.load(f)

links_withcomments = []
#para cada restaurante, recuperar las paginas de comentarios existentes
for i in tqdm(range(len(links))):
    link = links[i]
    partes = link.split('/')
    base = '/'.join(partes[:-1])

    a = requests.get(link, timeout=120)
    print(link)
    soup = BeautifulSoup(a.content)
    #get the pagination
    pages = soup.findAll("div", {"class":"pageNumbers"})
    
    #the first is the pagination of desired comments
    
    if(len(pages)>1):
        s_page = BeautifulSoup(str(pages[0]))
        nums = s_page.findAll('a')
        #get the last pagination number and link
        last_page = int(nums[-1].text)
        last_page_index = nums[-1]["href"]
        first_page_index = nums[0]["href"]

        print(first_page_index)
        print(last_page)
        print(last_page_index)

        for m in range(last_page):
            val = m*10
            link_rev = first_page_index.replace('Reviews', 'Reviews-or'+str(val))
            print(link_rev)
            links_withcomments.append(base+link_rev)
    
with open('../data/links_restaurants_revs.json', 'w') as out:
    json.dump(links_withcomments, out)
