import requests
import pandas as pd
import numpy as np
import urllib.parse

from config.config import API_URL, AUTH_HEADERS

class Player:
    
    def __init__(self, tag):
        self.tag = urllib.parse.quote(tag)
        self.info = {}
        self.cards = {}
        self.meanlevel = None
    
    def update(self):
        info_url = "%s/%s/%s" % (API_URL, 'players', self.tag)
        resp = requests.request("GET", info_url, headers=AUTH_HEADERS)
        if resp.status_code == 200:
            self.info = resp.json()
            self.cards = self.info['cards']
            tmp = []
            for card in self.cards:
                tmp.append(13-card['maxLevel']+card['level'])
            self.meanlevel = np.mean(tmp)
    
    def get_info(self):
        if self.info:
            return self.info
        else:
            print('Please update info!')
    
    def get_meanlevel(self):
        if self.meanlevel:
            return self.meanlevel
        else:
            print('Please update info!')
    
    def get_cards(self):
        if self.cards:
            return self.cards
        else:
            print('Please update info!')