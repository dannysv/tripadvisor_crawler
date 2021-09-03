import json
import sys
from utils.utils import *

def main(sufixo):
    path = '../data_'+sufixo+'/links_pagination_revs.json'
    path_out = '../data_'+sufixo+'/links_restaurants_revs.json'
    mdict, erro = read_json(path)
    link_revs = []
    if mdict is not None:
        for key in mdict.keys():
            link_revs += mdict[key]['pagination']
    else:
        print(erro)

    write_json(path_out, link_revs)

if __name__=='__main__':
    sufixo = sys.argv[1]
    main(sufixo)
