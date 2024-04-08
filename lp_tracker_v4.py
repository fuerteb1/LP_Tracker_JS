#   TODO Ideen
#   #tag zur json hinzufuegen
#   
#
#

import requests as req
import json
from flask import Flask
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/lp_tracker_v4.py": {"origins": "*"}}) # Fuegt CORS-Unterstuetzung hinzu (Flask extra fuer XMLHTTPRequest Fehler installiert)
app.config['CORS_HEADERS'] = 'Content-Type'


api_key = 'RGAPI-9c168d07-edc6-445d-ac8d-192930ee93fc'

    # summoner_id: J6qEG9dXncGiZNcX4GgFNAvUu_PXv5B2SvbC5m-pZONFjhU
    # puuid: Bz7KhrsR9of44GqKI49hd6LZcW0Dl9npLP5kT4Fif8spBNZziNGxv2uIyqVSx5rDhtOZttWKcySnKw


    ##################################   Player + Creation   ###########################################

class Player:

    def __init__(self, name, summoner_id, rank):
        self.__name = name
        self.__summoner_id = summoner_id
        self.__solo_rank = {'tier': None, 'rank': None, 'lp': None, 'lp_number': None} # Spieler rank ist immer nur der aktuelle Rang
        if len(rank['solo']) != 0:
            self.__solo_rank = {
                'tier': rank['solo'][0],
                'rank': rank['solo'][1],
                'lp': rank['solo'][2],
                'lp_number': rank_to_lp_number(rank['solo'])
            }
        self.__flex_rank = {'tier': None, 'rank': None, 'lp': None, 'lp_number': None}
        if len(rank['flex']) != 0:
            self.__solo_rank = {
                'tier': rank['flex'][0],
                'rank': rank['flex'][1],
                'lp': rank['flex'][2],
                'lp_number': rank_to_lp_number(rank['flex'])
            }
            
    def __str__(self): # Darstellung fuer Umwandlung str(Player)
        solo_rank, flex_rank = '[unranked]', '[unranked]'
        if self.is_ranked_solo():
            solo_rank = self.__solo_rank
        if self.is_ranked_flex():
            flex_rank = self.__flex_rank
        return f'Name: {self.__name}, SummonerID: {self.__summoner_id}, Rang Solo: {solo_rank}, Rang Flex: {flex_rank}'
    

    def is_ranked_solo(self):
        if self.__solo_rank['rank'] != None:
            return True
        else:
            return False
        
    def is_ranked_flex(self):
        if self.__flex_rank['rank'] != None:
            return True
        else:
            return False

    def update_rank(self): # nur updaten, falls der gefundene Rang unterschiedlich zum letzten gespeicherten Rang ist
        new_rank = find_rank_info(self.__summoner_id) 
        if len(new_rank['solo']) != 0: # es gibt einen neuen Eintrag fuer soloq / Spieler ist eingeranked
            if rank_to_lp_number(new_rank['solo']) != self.__solo_rank['lp_number']: # die lp_number des Spielers hat sich veraendert, also wird der rank geupdated
                self.__solo_rank = {
                'tier': new_rank['solo'][0],
                'rank': new_rank['solo'][1],
                'lp': new_rank['solo'][2],
                'lp_number': rank_to_lp_number(new_rank['solo']) # update auch LP Nummer, wenn Rang sich aendert
            } 
        if len(new_rank['flex']) != 0:
            if rank_to_lp_number(new_rank['flex']) != self.__flex_rank['lp_number']:
                self.__flex_rank = {
                'tier': new_rank['flex'][0],
                'rank': new_rank['flex'][1],
                'lp': new_rank['flex'][2],
                'lp_number': rank_to_lp_number(new_rank['flex'])
            } 
        
    # wird nur genutzt, wenn im player_list.json schon ein Eintrag zu diesem Spieler existiert
    # gibt unter 'tier', 'rank', etc nur einzelne Werte aus, die dann der Liste im player_list.json hinzugefuegt werden
    def player_to_json(self): 
        json_data = {
            'name': self.__name,
            'summoner_id': self.__summoner_id,
            'solo': self.solo_to_json(),
            'flex': self.flex_to_json()
        }
        return json_data
    
    def solo_to_json(self): 
        solo_data = { 'tier': [], 'rank': [], 'lp': [], 'lp_number': [] } # falls nicht eingeranked, leere Listen als Werte
        if self.is_ranked_solo():
            solo_data = {
                'tier': self.__solo_rank['tier'],
                'rank': self.__solo_rank['rank'],
                'lp': self.__solo_rank['lp'],
                'lp_number': self.__solo_rank['lp_number']
            }
        return solo_data
    
    def flex_to_json(self): 
        flex_data = { 'tier': [], 'rank': [], 'lp': [], 'lp_number': [] }
        if self.is_ranked_flex():
            flex_data = {
                'tier': self.__flex_rank['tier'],
                'rank': self.__flex_rank['rank'],
                'lp': self.__flex_rank['lp'],
                'lp_number': self.__flex_rank['lp_number']
            }
        return flex_data
    
    
    def new_player_to_json(self): #erstellt die Werte bei 'tier', 'rank', etc als Listen, damit spaeter neue Werte hinzugefuegt werden koennen
        json_data = {
            'name': self.__name,
            'summoner_id': self.__summoner_id,
            'solo': self.new_solo_to_json(),
            'flex': self.new_flex_to_json()
        }
        return json_data
        

    def new_solo_to_json(self):
        solo_data = { 'tier': [], 'rank': [], 'lp': [], 'lp_number': [] }
        if self.is_ranked_solo():
            solo_data = {
                'tier': [self.__solo_rank['tier']],
                'rank': [self.__solo_rank['rank']],
                'lp': [self.__solo_rank['lp']],
                'lp_number': [self.__solo_rank['lp_number']]
            }
        return solo_data
        
    def new_flex_to_json(self): 
        flex_data = { 'tier': [], 'rank': [], 'lp': [], 'lp_number': [] }
        if self.is_ranked_flex():
            flex_data = {
                'tier': [self.__flex_rank['tier']],
                'rank': [self.__flex_rank['rank']],
                'lp': [self.__flex_rank['lp']],
                'lp_number': [self.__flex_rank['lp_number']]
            }
        return flex_data

    # getter-Methoden
    def get_name(self):
        return self.__name
    def get_summoner_id(self):
        return self.__summoner_id
    def get_solo_rank(self):
        return self.__solo_rank
    def get_flex_rank(self):
        return self.__flex_rank
    
    


    
def create_new_player(name, tag):

    p_uuid = find_acc_uuid(name, tag) # finden die Infos fuer einen neuen Spieler, der folgend damit erstellt werden soll
    summoner_id = find_summoner_id(p_uuid)
    rank_info = find_rank_info(summoner_id)

    new_player = Player(name, summoner_id, rank_info)
    print('created new player')

    return new_player




#####################################   General Functions   ########################################


def get_input_name(inp): # Methode zur Eingabe des Namens durch Nutzer
    split_name = None
        
    if inp == 'skip':
        split_name = 'skip'
    elif inp == 'end' or '':
        split_name = 'end'
    if inp.find('#') != -1 and inp.find('#') != (len(inp) - 1):
        split_name = inp.split('#')
        if not does_acc_exist(split_name[0], split_name[1]):
            split_name = 'error'
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


def update_json(players, json_name='player_list.json'): # vergleicht Datensatze der gespeicherten Spieler mit den aktuellen und fuegt neue Werte hinzu
    with open(json_name) as j: # TODO Dateinamen aendern
        complete_json = json.load(j)
        summoner_ids = [ps['summoner_id'] for ps in complete_json['players']]

        for p in players:
            if summoner_ids.count(p.get_summoner_id()) == 0: # Diese Summoner_id ist noch nicht in der json Datei angelegt. Dann neuen 'player' zur json hinzufuegen
                p_json = p.new_player_to_json()
                complete_json['players'].append(p_json)

            else: # ein Eintrag zu diesem Spieler existiert bereits, pruefe ob er geupdated werden muss. Update den Eintrag falls noetig
                ind = summoner_ids.index(p.get_summoner_id()) # dem wie vielten Spieler unter 'players' gehoert diese summoner_id
                if p.is_ranked_solo(): # es bedarf nur einem Update, falls der Spieler eingeranked ist
                    old_solo_lp_number = complete_json['players'][ind]['solo']['lp_number']
                    if (old_solo_lp_number == []) or (old_solo_lp_number[-1] != p.get_solo_rank()['lp_number']): 
                    # der Spieler war vorher nicht eingeranked / neuer Rang unterscheidet sich vom alten:  jetzigen Wert zur Liste einfuegen
                        complete_json['players'][ind]['solo']['tier'].append(p.get_solo_rank()['tier'])
                        complete_json['players'][ind]['solo']['rank'].append(p.get_solo_rank()['rank'])
                        complete_json['players'][ind]['solo']['lp'].append(p.get_solo_rank()['lp'])
                        complete_json['players'][ind]['solo']['lp_number'].append(p.get_solo_rank()['lp_number'])
                if p.is_ranked_flex(): 
                    old_flex_lp_number = complete_json['players'][ind]['flex']['lp_number']
                    if (old_flex_lp_number == []) or (old_flex_lp_number[-1] != p.get_flex_rank()['lp_number']): # update falls noetig flex rank
                        complete_json['players'][ind]['flex']['tier'].append(p.get_flex_rank()['tier'])
                        complete_json['players'][ind]['flex']['rank'].append(p.get_flex_rank()['rank'])
                        complete_json['players'][ind]['flex']['lp'].append(p.get_flex_rank()['lp'])
                        complete_json['players'][ind]['flex']['lp_number'].append(p.get_flex_rank()['lp_number'])
                
    with open(json_name, 'w') as aw:
        json.dump(complete_json, aw, indent=4, ensure_ascii=False)

    print('gespeichert')    




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
    if 'status' in player_info.keys(): # falls Name nicht existiert steht in der json der FehlerSTATUS
        return False
    else:
        return True

def find_acc_uuid(name, tag): # 
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
        else:
            rank_solo = [p_info[1]['tier'], p_info[1]['rank'], p_info[1]['leaguePoints']]
            rank_flex = [p_info[0]['tier'], p_info[0]['rank'], p_info[0]['leaguePoints']]
        rank_info = {'solo': rank_solo, 'flex': rank_flex}

    elif len(p_info) == 1:
        if p_info[0]['queueType'] == 'RANKED_SOLO_5x5':
            rank_solo = [p_info[0]['tier'], p_info[0]['rank'], p_info[0]['leaguePoints']]
            rank_info = {'solo': rank_solo, 'flex': []}
        else:
            rank_flex = [p_info[0]['tier'], p_info[0]['rank'], p_info[0]['leaguePoints']]
            rank_info = {'solo': [], 'flex': rank_flex}
    
    return rank_info # {'solo': ['EMERALD', 'IV', 32], 'flex': []}  (flex ist hier unranked)



###################################   Main Methode  ################################################


def main(input):

    input_name = get_input_name(input) # Spieler, der durch Input geupdated werden soll
    input_player = create_new_player(input_name[0], input_name[1])

    input_player.update_rank()
    print('')
    print('Spieler: ' + str(input_player.get_name()))

    update_json([input_player])





#############################   JavaScript Request   ###############################################




@app.route('/lp_tracker_v4.py', methods=['POST'])
def lp_tracker_v4():
    print(str(request))
    input_value = request.json['params'] # Der Uebergabeparameter des Requests als json
    main(input_value)

    # print(str(request.json['params']))
    print('working')
    return 'success'
    
       

        
        
            
    # aufgrufener Code
if __name__ == '__main__':
    app.run(host='localhost', port=8000)
