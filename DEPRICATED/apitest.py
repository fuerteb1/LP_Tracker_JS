import requests as req


api_key = 'RGAPI-120eccd4-fcc4-4a76-9132-1743159f79df'
api_url = 'https://euw1.api.riotgames.com/lol/league-exp/v4/entries/RANKED_SOLO_5x5/PLATINUM/I?page=1'
myreq = api_url + '&api_key=' + api_key

resp = req.get(myreq)
info = resp.json()
print('')
print(len(info))
