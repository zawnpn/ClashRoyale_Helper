import os
import pickle
import requests
import pandas as pd
import urllib.parse
from datetime import datetime, timedelta

from config.config import API_URL, AUTH_HEADERS
from core.Player import Player

class Clan:
    
    def __init__(self, tag):
        self.tag = urllib.parse.quote(tag)
        self.info = {}
        self.warlog = {}
        self.members = []
        self.summary = None
        self.week_summary = None
        self.daily_summary = None
        self.flag = None
    
    def update(self):
        info_url = "%s/%s/%s" % (API_URL, 'clans', self.tag)
        resp = requests.request("GET", info_url, headers=AUTH_HEADERS)
        if resp.status_code == 200:
            self.info = resp.json()
    
    def update_summary(self):
        result = {}
        for member_info in self.info['memberList']:
            self.members.append(Player(member_info['tag']))
        for m in self.members:
            m.update()
            info = m.get_info()
            result[info['tag']] = {'Name': info['name'], 'KingLevel': info['expLevel'], 'Avg. CardLevel': m.get_meanlevel()}
        result = pd.DataFrame(result).T.sort_values(by='Avg. CardLevel',ascending=False)
        self.summary = result
    
    def update_warsummary(self):
        war_url = "%s/%s/%s/%s" % (API_URL, 'clans', self.tag, 'currentriverrace')
        resp = requests.request("GET", war_url, headers=AUTH_HEADERS)
        if resp.status_code == 200:
            self.warlog = resp.json()
            war_date = datetime.now() - timedelta(hours=18)
            timestamp = war_date.strftime("%Y/%m/%d")
            if war_date.month == 1 and war_date.strftime('%V') != '01':
                flag = '%s_%s' % (war_date.year - 1, war_date.strftime('%V'))
            else:
                flag = '%s_%s' % (war_date.year, war_date.strftime('%V'))

            pkl_file = 'result/' + flag + '.pkl'

            if os.path.exists(pkl_file):
                with open(pkl_file, 'rb') as f:
                    result = pickle.load(f)
            else:
                result = {}

            for p in self.warlog['clan']['participants']:
                p_k = '%s (%s)' % (p['name'], p['tag'])
                if p_k not in result.keys():
                    result[p_k] = {}
                result[p_k][timestamp] = p['fame']
            with open(pkl_file, 'wb') as f:
                pickle.dump(result, f)

            week_summary = pd.DataFrame(result).T
            week_summary = week_summary.sort_values(by=timestamp , ascending=False)
            # week_summary.to_excel('result/summary_' + flag + '.xlsx')

            daily_summary = pd.DataFrame([])
            for i in range(len(week_summary.columns) - 1):
                tmp = week_summary.iloc[:, i + 1] - week_summary.iloc[:, i]
                if daily_summary.empty:
                    daily_summary = tmp
                else:
                    daily_summary = pd.concat([daily_summary, tmp], axis=1)
            daily_summary.columns = week_summary.columns[1:]
            # daily_summary.to_excel('result/daily_' + flag + '.xlsx')
            self.week_summary = week_summary
            self.daily_summary = daily_summary
            self.flag = flag
        
    
    def get_info(self):
        if self.info:
            return self.info
        else:
            print('Please update info!')
    
    def get_summary(self):
        return self.summary
    
    def get_warsummary(self):
        return self.week_summary, self.daily_summary, self.flag
