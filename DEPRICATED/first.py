import matplotlib.pyplot as plt
import time
import threading as thr
import json 




class Player:

    def __init__(self, name, summoner_id, rank_s, rank_f):
        self.__name = name
        self.__summoner_id = summoner_id
        self.__solo_rank = {'tier': rank_s[0], 'rank': rank_s[1], 'lp': rank_s[2], 'lp_number': rank_s[3]} # Spieler rank ist immer nur der aktuelle Rang        
        self.__flex_rank = {'tier': rank_f[0], 'rank': rank_f[1], 'lp': rank_f[2], 'lp_number': rank_f[3]}
        
    def get_solo_rank(self):
        return self.__solo_rank







data = {
    'players': [
        {
            'name': 'fuerteb',
            'summoner_id': 123,
            'solo': {
                'tier': ['EMERALD'],
                'rank': ['IV'],
                'lp': [3],
                'lp_number': [2003]
            },
            'flex': {
                'tier': ['PLATINUM'],
                'rank': ['II'],
                'lp': [42],
                'lp_number': [1842]
            }

        },
        {
            'name': 'Deezyy',
            'summoner_id': 999,
            'solo': {
                'tier': ['MASTER'],
                'rank': ['I'],
                'lp': [280],
                'lp_number': [3080]
            },
            'flex': {
                'tier': ['DIAMOND'],
                'rank': ['III'],
                'lp': [94],
                'lp_number': [2594]
            }

        }
    ]
}

#with open('awesome.json', 'w') as d:
 #   json.dump(data, d, indent=3, ensure_ascii=False)

#new_file = open('awesome.json', 'w')    
#json.dump(data, new_file, indent=4, ensure_ascii=False)


#with open('awesome.json') as a:
#    new_data = json.load(a)



#summoner_ids = [p['summoner_id'] for p in new_data['players']]
#print(str(summoner_ids))


with open('awesome.json') as aw:
    complete_json = json.load(aw)


summoner_ids = [ps['summoner_id'] for ps in complete_json['players']]
print('ids: ' + str(summoner_ids))

value = summoner_ids.count()
print(str(value))

Macku = Player('Macku', 1999, ['EMERALD', 'I', 99], ['GOLD', 'III', 21])