from bs4 import BeautifulSoup
import re, os, requests

#change working directory
os.chdir(r"C:\Users\david\Phan_DSPN_S23\Phan_DSPN_S23_Final\Decks")

#read event ids from mtgtop8 url
def getevents(url):
    req = requests.get(url)
    data = BeautifulSoup(req.content,'html.parser')
    #get table containing 20 most recent events
    table = data.findAll("table")[2]
    #get event ids
    eventlist = list(set(re.findall("event.+?(?=\")",str(table))))
    return eventlist

#download all decklists from a single event
def getdecks(decks,format,n):
    for deck in decks:
        deckid = "mtgo?" + deck.split("&")[1]
        name = format + "deck" + str(n)
        link = "https://mtgtop8.com/" + deckid
        req = requests.get(link,allow_redirects=True)
        open(name,'wb').write(req.content)
        n += 1
    return n

#download decklists from 20 most recent events
def download(eventlist):
    n = 1
    format = str(eventlist[0].split("f=")[1])
    for event in eventlist:
        link = "https://mtgtop8.com/" + event
        eventdata = requests.get(link).text
        #find deck ids
        eventdata = re.findall("margin:0px 4px 0px 4px[\S\s]*?c_bl",
                                eventdata)[0]
        decks = list(set(re.findall("href=\?.*?(?=>)",eventdata)))
        n = getdecks(decks,format,n)

#combine funcs
def run(url):
    eventlist = getevents(url)
    download(eventlist)