import csv, json, os, regex
import pandas as pd

os.chdir("C:/Users/david/Phan_DSPN_S23/DSPN_Final/Data")
with open("RelevantCards") as file:
    cards = json.load(file)

#get correct MV category
def MV_cat(cat,card):
    if float(cards[cat][card]) >= 6:
        return 'MV6+'
    else:
        return 'MV' + str(int(cards[cat][card]))

#analyze decklist
def categorize(deck):
    dict = {}
    dict['lands'] = 0
    dict['mdfcs'] = 0
    dict['cantrips'] = 0
    dict['ramp'] = 0
    dict['other'] = 0
    dict['companion'] = 0
    dict['decksize'] = 0
    dict['MV'] = 0
    dict['MV0'] = 0
    dict['MV1'] = 0
    dict['MV2'] = 0
    dict['MV3'] = 0
    dict['MV4'] = 0
    dict['MV5'] = 0
    dict['MV6+'] = 0
    #split mainboard and sideboard
    if 'Sideboard' in deck:
        mainboard = deck[:deck.index('Sideboard')]
        sideboard = deck[deck.index('Sideboard')+1:]
    else:
        mainboard = deck
        sideboard = []
    #categorize cards in mainboard
    for line in mainboard:
        count = float(line.split(" ",1)[0])
        card = line.split(" ",1)[1]
        card = card.split(" / ")[0]
        dict['decksize'] += count
        for cat in cards:
            if card in cards[cat]:
                dict[cat] += float(count)
                dict[MV_cat(cat,card)] += float(count)
                dict['MV'] += count * float(cards[cat][card])
                break
    #check for companion
    for line in sideboard:
        card = line.split(" ",1)[1]
        if card in cards['companions']:
            dict['companion'] = 1
            break
    return list(dict.values())


#categorize training set decklists
deck_data = pd.DataFrame(columns = ['lands',
                                'mdfcs',
                                'cantrips',
                                'ramp',
                                'other',
                                'companion',
                                'decksize',
                                'MV',
                                'MV0',
                                'MV1',
                                'MV2',
                                'MV3',
                                'MV4',
                                'MV5',
                                'MV6plus',
                                'archetype',
                                'format'])

for filename in os.listdir("Decks"):
    decklist = open("Decks/" + filename)
    decklist = decklist.readlines()
    #remove newlines
    decklist = [line.replace('\n', '') for line in decklist]
    split = regex.split("\d+_",filename)
    arche = split[1]
    format = split[0]
    deck_data.loc[filename] = categorize(decklist) + [arche] + [format]

filename = "deck_data"
deck_data.to_csv(filename)