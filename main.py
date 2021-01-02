from core.Player import Player
from core.Clan import Clan

if __name__ == "__main__":
    clans = {}
    clans['a'] = Clan('#2QVCUYQR') # fill in the clan's name and tag
    # clans['b'] = Clan('#BBBBBBB') # store more clans

    for _,clan in clans.items():
        clan.update()
    
    # # get clan's summary in DataFrame format
    # clans['a'].update_summary()
    # summary = clans['a'].get_summary()
    # summary.to_excel('result/summary.xlsx')

    # get clan's war_summary in DataFrame format
    clans['a'].update_warsummary()
    week_summary, daily_summary, flag = clans['a'].get_warsummary()
    week_summary.to_excel('result/week_' + flag + '.xlsx')
    daily_summary.to_excel('result/daily_' + flag + '.xlsx')
