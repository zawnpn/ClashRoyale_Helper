import requests
import pandas as pd
import urllib.parse

from config.config import API_URL, AUTH_HEADERS
from core.Player import Player

class Clan:
    
    def __init__(self, tag):
        self.tag = urllib.parse.quote(tag)
        self.info = {}
        self.warlog = {}
        self.members = []
        self.summary = None
        self.warsummary = None
    
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
        war_url = "%s/%s/%s/%s" % (API_URL, 'clans', self.tag, 'warlog')
        resp = requests.request("GET", war_url, headers=AUTH_HEADERS)
        if resp.status_code == 200:
            self.warlog = resp.json()
            result = {}
            for i in self.warlog['items']:
                for p in i['participants']:
                    if p['tag'] in result.keys():
                        result[p['tag']]['Wins'] += p['wins']
                        result[p['tag']]['FinalPlayed'] += p['battlesPlayed']
                        result[p['tag']]['Final'] += p['numberOfBattles']
                        result[p['tag']]['CollectPlayed'] += p['collectionDayBattlesPlayed']
                        result[p['tag']]['Collect'] += 3
                    else:
                        result[p['tag']] = {
                            'Name': p['name'], 
                            'Wins': p['wins'], 
                            'FinalPlayed': p['battlesPlayed'], 
                            'Final': p['numberOfBattles'],
                            'CollectPlayed': p['collectionDayBattlesPlayed'],
                            'Collect': 3,
                        }
            for _,r in result.items():
                r['WinRate'] = r['Wins']/r['Final']
                r['Attendance'] = r['FinalPlayed']/r['Final']
                r['CollectAttendance'] = r['CollectPlayed']/r['Collect']
            
            result = pd.DataFrame(result).T.sort_values(by='WinRate',ascending=False)
            self.warsummary = result
    
    def get_info(self):
        if self.info:
            return self.info
        else:
            print('Please update info!')
    
    def get_summary(self):
        return self.summary
    
    def get_warsummary(self):
        return self.warsummary