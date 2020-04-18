from core.Player import Player
from core.Clan import Clan

if __name__ == "__main__":
    clans = {}
    clans['a'] = Clan('#AAAAAAA') # fill in the clan's name and tag
    # clans['b'] = Clan('#BBBBBBB') # store more clans

    for _,clan in clans.items():
        clan.update()
    
    # get clan's summary in DataFrame format
    clans['a'].update_summary()
    summary = clans['a'].get_summary()
    summary.to_excel('summary.xlsx')

    # get clan's war_summary in DataFrame format
    clans['a'].update_warsummary()
    war_summary = clans['a'].get_warsummary()
    war_summary.to_excel('war_summary.xlsx')

