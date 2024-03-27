import requests as req
import threading
import time
import matplotlib.pyplot as plt


# fuerteb puuid: Bz7KhrsR9of44GqKI49hd6LZcW0Dl9npLP5kT4Fif8spBNZziNGxv2uIyqVSx5rDhtOZttWKcySnKw
api_key = 'RGAPI-93d90fb5-f571-4c43-b6b0-3dee84650a41'
request_start_str = '?api_key='
request_add_str = '&api_key='
looping = 'true'
rank_list = []


class Player:
    def __init__(self, name, summoner_id, rank_list):
        self.name = name
        self.summoner_id = summoner_id
        self.rank_list = rank_list

    def __str__(self):
        return f'Name: {self.name}, SummonerID: {self.summoner_id}, Rang: {self.rank_list[-1]}'


def create_uuid_url(region, name, tag, api_key): # link zum finden der player uuid generieren
    # Beispiel: https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/fuerteb/EUW
    ret_str = (
        'https://' +
        region +
        '.api.riotgames.com/riot/account/v1/accounts/by-riot-id/' +
        name +
        '/' +
        tag +
        '?api_key=' +
        api_key
    )
    return ret_str


def get_acc_uuid():    # Name, Tag + Region erhalten und dazugehoerige player uuid finden
    eingabe = str(input('Namen und #Tag zusammen (ohne Leerzeichen dazwischen) eingeben: '))
    print('Deine Eingabe: ' + eingabe) # TODO print entfernen
    name = eingabe.split('#')[0]
    tag = eingabe.split('#')[1]
    region = 'europe'
    # fuer spezifisches Festlegen der Region. Fuer jetzt nur EUW, da Server != Region ist
    '''  (  eingabe = '' 
    while ("eu" or "na" or "as") not in eingabe:
        eingabe = input('Region waehlen: "EU", "NA" oder "AS":')
        eingabe = eingabe.lower()     
    if eingabe.find('as') != -1:
        region = 'asia'
    elif eingabe.find('na') != -1:
        region = 'americas'
    else:
        region = 'europe'  ) '''
    req_url = create_uuid_url(region, name, tag, api_key)
    p_info = req.get(req_url).json() # kann auch 
    if 'status' in p_info.keys() : # pruefe, ob Name ueberhaupt existiert
        print('-- Name nicht gefunden --')
        return 'Name nicht gefunden'
    return p_info['puuid']


def get_acc_info(puuid):
    req_url = (
        'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/' + # TODO funktioniert nur fuer EUW
        puuid +
        '?api_key=' +
        api_key
    )
    p_info = req.get(req_url).json()
    acc_info = {'name': p_info['name'], 'summoner_id': p_info['id']}
    return acc_info # {name, summoner_id}


def get_rank_info(summoner_id):
    req_url = (
        'https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/' + 
        summoner_id +
        '?api_key=' + 
        api_key
    )
    info_soloq, info_flex, rank_info = None, None, ''

    p_info = req.get(req_url).json() # legt nur Eintrag an, falls man eingeranked ist
    if len(p_info) == 2:
        if p_info[0]['queueType'] == 'RANKED_SOLO_5x5': # in der Json ist der hoehere Rank zuerst aufgefuehrt
            info_soloq = p_info[0]
            info_flex = p_info[1]
        else:
            info_soloq = p_info[1]
            info_flex = p_info[0]

        rank_info = ( # Beispiel: EMERALD, III, 60
        [[info_soloq['tier'],info_soloq['rank'], info_soloq['leaguePoints']], 
        [info_flex['tier'], info_flex['rank'], info_flex['leaguePoints']]]
        ) 

    elif len(p_info) == 1:
        if p_info[0]['queueType'] == 'RANKED_SOLO_5x5':
            info_soloq = p_info[0]
            rank_info = [[info_soloq['tier'],info_soloq['rank'], info_soloq['leaguePoints']],[]]
        else:
            info_flex = p_info[0]
            rank_info = [[], [info_flex['tier'], info_flex['rank'], info_flex['leaguePoints']]]
        
    else: # in keiner Queue eingeranked
        rank_info = ' ist in keiner Queue eingeranked'
    
    return rank_info



def looping_rank_check(uuid):
    while looping != 'n':
        time.sleep(2400) # TODO Zeit veraendern
        rank_info = get_rank_info(get_acc_info(uuid)['summoner_id'])
        print('x') #TODO entfernen
        if len(rank_info) == 2:
            print('SoloQ: ' + str(rank_info[0]) + ', Flex: ' + str(rank_info[1]))
        else:
            print(str(rank_info))

def list_of_ranks(rank_list, new_rank):
    if rank_list[-1] is not new_rank:
        rank_list.extend(new_rank)
    return rank_list

def plot_rank(name, rank_list): # TODO
    plt.ion()
    plt.plot(rank_list)
    plt.show()

def main():
    response = ''
    while(response.lower() != 'n'):
        print('---------- new Input ------------')

        acc_uuid = get_acc_uuid()
        if acc_uuid == 'Name nicht gefunden': # ueberspringt den restlichen Code, falls acc_uuid nicht gefunden werden konnte
            continue
        
        loop_checker = threading.Thread(target=looping_rank_check, daemon=True, args=(acc_uuid,))
        loop_checker.start()

        acc_info = get_acc_info(acc_uuid) # dict fuer name + summoner_id

        rank_info = get_rank_info(acc_info['summoner_id'])
        if len(rank_info) == 2:
            print(acc_info['name'] + ': SoloQ: ' + str(rank_info[0]) + ', Flex: ' + str(rank_info[1]))
        else:
            print(acc_info['name'] + ': ' + str(rank_info))

        print('')
        response = str(input('Nochmal? Tippe "n" zum beenden, sonst einfach ENTER druecken: '))
            



main()







