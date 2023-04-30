import os, requests, json

os.chdir(r"C:\Users\david\Phan_DSPN_S23\DSPN_Final\Data")

#retrieve cards
def gather(link,dict):
    data = requests.get(link)
    data = data.json()
    #add card name and mana value to cards
    for card in data['data']:
        name = card['name'].split(" // ")[0]
        mv = card['cmc']
        if (name not in cards.values()) or (dict == cards['companion']):
            dict[name] = mv
    #go to the next page if there is one, otherwise stop
    if data['has_more'] == False:
        return
    else:
        gather(data['next_page'],dict)

#create dictionary
cards = {}
cards['lands'] = {}
cards['mdfcs'] = {}
cards['cantrips'] = {}
cards['ramp'] = {}
cards['other'] = {}
cards['companions'] = {}

#get normal lands
link = "https://api.scryfall.com/cards/search?q=(legal:pioneer+or+banned:pioneer+or+legal:historic+or+banned:historic)+t:land+mv:0&order=name"
gather(link,cards['lands'])

#get mdfc lands
link = "https://api.scryfall.com/cards/search?q=is:mdfc+t:land+mv>0&order=name"
gather(link,cards['mdfcs'])

#get cantrips
link = "https://api.scryfall.com/cards/search?q=(legal:pioneer+or+banned:pioneer+or+legal:historic+or+banned:historic)+t:creature+mv<=2+fo:'when'+fo:'enters'+fo:'draw'+-fo:'investigate'+-fo:'blood'&order=name"
gather(link,cards['cantrips'])

link = "https://api.scryfall.com/cards/search?q=(legal:pioneer+or+banned:pioneer+or+legal:historic+or+banned:historic)+-t:creature+-t:land+mv<=2+((fo:'look'+fo:'library'+fo:'put'+fo:'hand'+-fo:'pay')+or+(fo:'draw'+-fo:'investigate'+-fo:'blood'))&order=name"
gather(link,cards['cantrips'])

link = "https://api.scryfall.com/cards/search?q=(legal:pioneer+or+banned:pioneer+or+legal:historic+or+banned:historic)+(fo:'cycling+{1}+'+or+fo:'cycling+{w}'+or+fo:'cycling+{u}'+or+fo:'cycling+{b}'+or+fo:'cycling+{r}'+or+fo:'cycling+{g})&order=name"
gather(link,cards['cantrips'])

#get ramp cards
link = "https://api.scryfall.com/cards/search?q=(legal:pioneer+or+banned:pioneer+or+legal:historic+or+banned:historic)+mv<=2+-t:land+is:permanent+fo:'add+'+-fo:'add+its+ability'+-fo:'add+a+lore+counter'+-fo:'dies'&order=name"
gather(link,cards['ramp'])

link = "https://api.scryfall.com/cards/search?q=(legal:pioneer+or+banned:pioneer+or+legal:historic+or+banned:historic)+mv<=2+-t:land+((fo:'search'+fo:'library'+(fo:'land'+or+fo:'basic')+-fo:'sacrifice')+or+(fo:'enchanted+land+is+tapped'+fo:'adds+an+additional')+or+(fo:'put+a+creature+card+with'+fo:'from+your+hand+onto+the+battlefield'))&order=name"
gather(link,cards['ramp'])

#get everything else
link = "https://api.scryfall.com/cards/search?q=(legal:pioneer+or+banned:pioneer+or+legal:historic+or+banned:historic)&order=name"
gather(link,cards['other'])

#get companions. don't want to exclude them since they can be in sideboard
link = "https://api.scryfall.com/cards/search?q=is:companion&order=name"
gather(link,cards['companions'])

#export list
json_cards = json.dumps(cards,indent=4)
with open("RelevantCards",'w') as file:
    file.write(json_cards)