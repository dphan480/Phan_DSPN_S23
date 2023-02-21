import os, requests, json

os.chdir(r"C:\Users\david\Phan_DSPN_S23\Phan_DSPN_S23_Final")

cardlist = {}
def gather(link):
    data = requests.get(link)
    data = data.json()
    #add card name, type, and mana value to cardlist
    for card in data['data']:
        name = card['name'].split(" //",1)[0]
        mv = card['cmc']
        type = card['type_line']
        if "Land" not in type:
            cardlist[name] = [mv,type]
    #go to the next page if there is one, otherwise stop
    if data['has_more'] == False:
        return
    else:
        gather(data['next_page'])

gather("https://api.scryfall.com/cards/search?order=name&q=legal%3Apioneer")

json_cardlist = json.dumps(cardlist,indent=4)
with open("PioneerLegalCards",'w') as file:
    file.write(json_cardlist)