import regex, os, requests
from bs4 import BeautifulSoup

#inputs for search form
inputs = {
    'compet_check[P]' : 'checked',
    'compet_check[M]' : 'checked',
    'date_start' : '01/03/2021',
    'format' : 'ST',
    'current_page' : 1
    }
formats = ['ST','EXP','PI''HI','ALCH']

#get deck ids
deck_ids = {}
for f in formats:
    inputs['format'] = f
    deck_ids[f] = []
    #loop through pages
    for page in range(1,70):
        inputs['current_page'] = page
        #extract deck ids
        html = requests.post('https://mtgtop8.com/search',data=inputs)
        soup = BeautifulSoup(html.content, 'html.parser')
        tables = soup.findAll('table')
        deck_ids[f].extend(regex.findall("event\?e=.+d=.+(?=\")",
                            str(tables[2])))

#fix ampersands
for format in deck_ids:
    for i in range(len(deck_ids[format])):
        deck_ids[format][i] = deck_ids[format][i].replace('amp;','')

#retrieve decklists using deck ids
os.chdir(r"C:\Users\david\Phan_DSPN_S23\DSPN_Final\Data\Decks")
for format in deck_ids:
    n = 1
    for id in deck_ids[format]:
        #get deck archetype
        html = requests.get('https://mtgtop8.com/' + id)
        soup = BeautifulSoup(html.content,'html.parser')
        arche = regex.findall('(?<=archetype.+>).+(?= decks)',str(soup))
        if len(arche) == 0:
            arche = "Other"
        else:
            arche = arche[0]
            arche = arche.replace("/","or")
            arche = arche.replace("-","")
            arche = arche.replace(" ","")
        #retrieve decklist
        url = 'https://mtgtop8.com/mtgo?' + id.split('&',1)[1]
        req = requests.get(url,allow_redirects=True)
        name = format + str(n) + "_" + arche
        open(name,'wb').write(req.content)
        print(name)
        n += 1