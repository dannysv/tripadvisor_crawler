import json
import requests
from bs4 import BeautifulSoup
import codecs
from tqdm import tqdm 

out = codecs.open('../data/reviews.txt', 'w')

links = []
with open('../data/links_restaurants_revs.json', 'r') as f:
    links = json.load(f)

#print(links)

for i in tqdm(range(len(links[:10]))):
#for i in range(1):
    link = links[i]
    a = requests.get(link, timeout=120)
    #print(link)
    soup = BeautifulSoup(a.content)
    comments = soup.findAll("div", {"class":"prw_rup prw_reviews_text_summary_hsx"})
    for comment in comments:
        #print(comment.text)
        out.write(comment.text)
