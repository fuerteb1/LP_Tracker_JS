import requests as req
import time
import json


api_key = 'RGAPI-15540f75-f952-49ef-8b3e-e868eb9a83c5'

# summoner_id: J6qEG9dXncGiZNcX4GgFNAvUu_PXv5B2SvbC5m-pZONFjhU
# puuid: Bz7KhrsR9of44GqKI49hd6LZcW0Dl9npLP5kT4Fif8spBNZziNGxv2uIyqVSx5rDhtOZttWKcySnKw


##################################   Player + Creation   ###########################################

class Player:

    def __init__(self, name, summoner_id, rank_list):
        self.__name = name
        self.__summoner_id = summoner_id
        self.__rank_list = rank_list # implementiert als Dictionary mit 2 keys ('solo' und 'flex') mit (String: Liste von Listen mit Ranks) -> rank_list: {'solo':['MASTER', 'I', 230], 'flex':['DIAMOND', II, 48 }
        self.__lp_list = {'solo': [], 'flex': []}
        if self.__is_ranked_solo():
            self.__lp_list['solo'].append(rank_to_lp_number(self.__rank_list['solo'][-1]))              # TODO PRINT
        if self.__is_ranked_flex():
            self.__lp_list['flex'].append(rank_to_lp_number(self.__rank_list['flex'][-1]))

        

    def __str__(self): # Darstellung fuer Umwandlung str(Player)
        solo_rank, flex_rank = '[unranked]', '[unranked]'
        if self.__is_ranked_solo():
            solo_rank = self.__rank_list['solo'][-1]
        if self.__is_ranked_flex():
            flex_rank = self.__rank_list['flex'][-1]
        return f'Name: {self.__name}, SummonerID: {self.__summoner_id}, Rang Solo: {solo_rank}, LP Liste: {self.__lp_list['solo']}, Rang Flex: {flex_rank}'
    
    def __is_ranked_solo(self):
        if len(self.__rank_list['solo']) > 0:
            return True
        else:
            return False
        
    def __is_ranked_flex(self):
        if len(self.__rank_list['flex']) > 0:
            return True
        else:
            return False

    def update_rank(self): # nur updaten, falls der gefundene Rang unterschiedlich zum letzten gespeicherten Rang ist
        new_rank = find_rank_info(self.__summoner_id) 
        if len(new_rank['solo']) != 0: # es gibt einen neuen Eintrag fuer soloq / Spieler ist eingeranked
            if len(self.__rank_list['solo']) == 0: # es gibt bisher keinen Eintrag fuer Soloq des Spielers
                self.__rank_list['solo'].append(new_rank['solo'])
                self.__lp_list['solo'].append(rank_to_lp_number(self.__rank_list['solo'][-1])) # update auch LP Liste, wenn Rang sich aendert
            
            elif new_rank['solo'][0] != self.__rank_list['solo'][-1]: # der alte und neue Eintrag sind verschieden
                self.__rank_list['solo'].append(new_rank['solo'][0])
                self.__lp_list['solo'].append(rank_to_lp_number(self.__rank_list['solo'][-1]))

        if len(new_rank['flex']) != 0:
            if len(self.__rank_list['flex']) == 0: 
                self.__rank_list['flex'].append(new_rank['flex'][0])
                self.__lp_list['flex'].append(rank_to_lp_number(self.__rank_list['flex'][-1]))
            elif new_rank['flex'][0] != self.__rank_list['flex'][-1]:
                self.__rank_list['flex'].append(new_rank['flex'][0])
                self.__lp_list['flex'].append(rank_to_lp_number(self.__rank_list['flex'][-1]))
    
    def player_to_list(self): # DEPRICATED
        player_list = [
            self.__name,
            self.__summoner_id,
            self.__rank_list, # {'solo': [['EMERALD', 'IV', 32], ['EMERALD', 'IV', 49]], 'flex': []
            self.__lp_list 
        ]

    def player_to_json(self):
        json_data = {
            'name': self.__name,
            'summoner_id': self.__summoner_id,
            'solo': {
                'tier': self.get_solo_tiers(),
                'rank': self.get_solo_ranks(),
                'lp': self.get_solo_lps(),
                'lp_number': self.get_solo_lp_lists()
            },
            'flex': {
                'tier': self.get_flex_tiers(),
                'rank': self.get_flex_ranks(),
                'lp': self.get_flex_lps(),
                'lp_number': self.get_flex_lp_lists()
            }
        }
        return json_data
    
    def solo_to_json(self):
        solo_data = {
            'tier': self.get_solo_tiers(),
            'rank': self.get_solo_ranks(),
            'lp': self.get_solo_lps(),
            'lp_number': self.get_solo_lp_lists()            
        }
        return solo_data
    
    def flex_to_json(self):
        flex_data = {
            'tier': self.get_flex_tiers(),
            'rank': self.get_flex_ranks(),
            'lp': self.get_flex_lps(),
            'lp_number': self.get_flex_lp_lists()      
        }
    
        
    # getter-Methoden
    def get_name(self):
        return self.__name
    def get_summoner_id(self):
        return self.__summoner_id
    def get_rank_list(self):
        return self.__rank_list
    def get_lp_list(self):
        return self.__lp_list
    
    def get_solo_tiers(self):
        vals = []
        for r in self.__rank_list['solo']:
            vals.append(r[0])
        return vals
    def get_solo_ranks(self):
        vals = []
        for r in self.__rank_list['solo']:
            vals.append(r[1])
        return vals
    def get_solo_lps(self):
        vals = []
        for r in self.__rank_list['solo']:
            vals.append(r[2])
        return vals
    def get_solo_lp_lists(self):
        vals = []
        for r in self.__lp_list['solo']:
            vals.append(r)
        return vals
    
    def get_flex_tiers(self):
        vals = []
        for r in self.__rank_list['flex']:
            vals.append(r[0])
        return vals
    def get_flex_ranks(self):
        vals = []
        for r in self.__rank_list['flex']:
            vals.append(r[1])
        return vals
    def get_flex_lps(self):
        vals = []
        for r in self.__rank_list['flex']:
            vals.append(r[2])
        return vals
    def get_flex_lp_lists(self):
        vals = []
        for r in self.__lp_list['flex']:
            vals.append(r)
        return vals

   
    
def create_new_player(name, tag):

    p_uuid = find_acc_uuid(name, tag) # finden die Infos fuer einen neuen Spieler, der folgend damit erstellt werden soll
    summoner_id = find_summoner_id(p_uuid)
    rank_info = find_rank_info(summoner_id)

    new_player = Player(name, summoner_id, rank_info)

    return new_player




#####################################   General Functions   ########################################

def get_input_name(): # Methode zur Eingabe des Namens durch Nutzer
    split_name = None
    while(True):
        print('')
        inp = str(input('Namen + #Tag zusammen (ohne Leerzeichen dazwischen) eingeben: ' ))
        if inp == 'skip':
            split_name = 'skip'
            break
        if inp.find('#') != -1 and inp.find('#') != (len(inp) - 1):
            split_name = inp.split('#')
            if does_acc_exist(split_name[0], split_name[1]):
                break
    return split_name


# rechnet Rang ['EMERALD', 'IV', 32] zu Zahl 2032 um
# jeder Rang 400 LP = Iron 0 bis 399 mit Iron IV 0 bis 99
def rank_to_lp_number(cur_rank):  
        cur_lp_number = 0
        match cur_rank[0]:
            case 'IRON': cur_lp_number += 0
            case 'BRONZE': cur_lp_number += 400
            case 'SILVER': cur_lp_number += 800
            case 'GOLD': cur_lp_number += 1200
            case 'PLATINUM': cur_lp_number += 1600
            case 'EMERALD': cur_lp_number += 2000
            case 'DIAMOND': cur_lp_number += 2400
            case 'MASTER' | 'GRANDMASTER' | 'CHALLENGER': cur_lp_number += 2800
        if cur_lp_number < 2800: # Master und hoeher sind immer in 'I'
            match cur_rank[1]:
                case 'IV': cur_lp_number += 0
                case 'III': cur_lp_number += 100
                case 'II': cur_lp_number += 200
                case 'I': cur_lp_number += 300
        
        cur_lp_number += cur_rank[2]
        return cur_lp_number


def all_players_to_json(players):
    player_json_list = []
    for p in players:
        player_json = p.player_to_json()
        player_json_list.append(player_json)
    
    all_json_list = { 'players': player_json_list }
    return all_json_list


def update_json(players): # vergleicht Datensatze der gespeicherten Spieler mit den aktuellen und fuegt neue Werte hinzu
    with open('awesome.json') as j: # TODO Dateinamen aendern
        complete_json = json.load(j)

        summoner_ids = [ps['summoner_id'] for ps in complete_json['players']]
        for p in players:
            if summoner_ids.count(p['summoner_id']) == 0: # Diese Summoner_id ist noch nicht in der json Datei angelegt. Dann neuen 'player' zur json hinzufuegen
                p_json = p.player_to_json()
                complete_json['players'].append(p_json)

            else: # ein Eintrag zu diesem Spieler existiert bereits, pruefe ob er geupdated werden muss
                ind = summoner_ids.index(p['summoner_id'])
                p_ranks = p.get_rank_list()
                if len(p_ranks['solo']) > 0: # Spieler ist eingeranked (in solo). Sonst bedarf es keinem Update
                    if len(complete_json['players'][ind]['solo']['tier']) == 0: # war vorher nicht eingeranked
                        complete_json['players'][ind]['solo'] = p.solo_to_json()
                    else: # war vorher eingeranked. Pruefe ob sich lp veraendert haben. Nur dann updaten
                        lp_number_new = p.get_lp_list()[-1]
                        lp_number_old = complete_json['players'][ind]['solo']['lp_number']
                        if lp_number_new != lp_number_old:
                            # neuer Rang unterscheidet sich vom alten, Problem: Werte sind in einer Liste gespeichert. Komplett durchlaufen?
                            # zu updaten: tier, rank, lp, lp_number
                            pass
########## TODO TODO TODO TODO TODO TODO #############




#####################################   API Access   ###############################################
    
def does_acc_exist(name, tag): # checkt, ob eingegebener Name ueberhaupt exisitert (aehnlich zu find_acc_uuid)
    region = 'europe'
    req_url = (
        'https://' +
        region +
        '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' +
        name +
        '/' +
        tag +
        '?api_key=' +
        api_key
    )
    player_info = req.get(req_url).json()
    if 'status' in player_info.keys(): # falls Name nicht existiert steht in der json der FehelerSTATUS
        return False
    else:
        return True

def find_acc_uuid(name, tag): # TODO
    region = 'europe' # spaeter noch auf andere Regionen erweiterbar
    req_url = (
        'https://' +
        region +
        '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' +
        name +
        '/' +
        tag +
        '?api_key=' +
        api_key
    )
    player_info = req.get(req_url).json()
    return player_info['puuid']


def find_summoner_id(puuid):
    req_url = (
        'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/' + # nur fuer EUW Server
        puuid +
        '?api_key=' +
        api_key
    )
    player_info = req.get(req_url).json()
    return player_info['id']


def find_rank_info(summoner_id): # return als Dict mit String : Liste von Listen {'solo': [Rang], 'flex': [Rang]}
    req_url = (
        'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + 
        summoner_id +
        '?api_key=' + 
        api_key
    )
    rank_solo, rank_flex, rank_info = [], [], {'solo': [], 'flex': []}
    p_info = req.get(req_url).json() # legt nur Eintrag an, falls man eingeranked ist

    if len(p_info) == 2:
        if p_info[0]['queueType'] == 'RANKED_SOLO_5x5': # in der Json ist der hoehere Rank zuerst aufgefuehrt
            rank_solo = [p_info[0]['tier'], p_info[0]['rank'], p_info[0]['leaguePoints']]
            rank_flex = [p_info[1]['tier'], p_info[1]['rank'], p_info[1]['leaguePoints']]
            rank_info = {'solo': [rank_solo], 'flex': [rank_flex]}
        else:
            rank_solo = [p_info[1]['tier'], p_info[1]['rank'], p_info[1]['leaguePoints']]
            rank_flex = [p_info[0]['tier'], p_info[0]['rank'], p_info[0]['leaguePoints']]
            rank_info = {'solo': [rank_solo], 'flex': [rank_flex]}
    elif len(p_info) == 1:
        if p_info[0]['queueType'] == 'RANKED_SOLO_5x5':
            rank_solo = [p_info[0]['tier'], p_info[0]['rank'], p_info[0]['leaguePoints']]
            rank_info = {'solo': [rank_solo], 'flex': []}
        else:
            rank_flex = [p_info[0]['tier'], p_info[0]['rank'], p_info[0]['leaguePoints']]
            rank_info = {'solo': [], 'flex': [rank_flex]}
    
    return rank_info









################################## Thread Ausfuehrung ##############################################


def looped_rank_check(players): # TODO sleep bzw. wiederholen alle 30min
    while True:
        time.sleep(10) # Zeit bis zum naechsten Reload
        print(players)
        for p in players:
            p.update_rank()
        






###################################   Main Methode  ################################################


def main():
    players = []
   

    while(True):
        input_name = get_input_name()
        if input_name != 'skip':
            players.append(create_new_player(input_name[0], input_name[1]))
        
        for p in players:
            
            p.update_rank()
            print('')
            print('Spieler: ' + str(p))

        with open('player_list.json', 'w') as doc:
            json.dump(all_players_to_json(players), doc, indent=3, ensure_ascii=False)



    
    
        
# aufgrufener Code

main()











