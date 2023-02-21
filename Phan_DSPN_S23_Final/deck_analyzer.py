import csv, json, os

with open("PioneerLegalCards") as file:
    cardlist = json.load(file)

#get average MV of nonland cards as well as land count (adjusted for 60 cards)
def avg_MV(decklist):
    nonland = 0
    land = 0
    MV = 0
    for line in decklist:
        card = line.split(" ",1)
        if card[1] in cardlist.keys():
            MV += float(card[0]) * float(cardlist[card[1]][0])
            nonland += float(card[0])
        else:
            land += float(card[0])
    avg = MV/nonland
    land = land * 60/(land+nonland)
    return [avg,land]

#get avg MV and land count for each deck
MV_Lands = []
n = 0
deck_count = len(os.listdir("Decks"))
while n < deck_count:
    #read decklist
    file = "Decks/" + os.listdir("Decks")[n]
    decklist = open(file)
    decklist = decklist.readlines()
    #remove newlines
    decklist = [line.replace('\n', '') for line in decklist]
    #remove sideboard
    if "Sideboard" in decklist:
        decklist = decklist[:decklist.index("Sideboard")]

    #add MV and landcount to list
    MV_Lands.append(avg_MV(decklist))
    n += 1

with open('MV_Lands.csv', 'w+', newline ='') as file:
    w = csv.writer(file)
    w.writerows(MV_Lands)