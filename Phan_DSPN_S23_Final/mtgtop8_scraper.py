from bs4 import BeautifulSoup

with open("Explorer events and metagame @ mtgtop8.com.html") as html:
    data = BeautifulSoup(html, 'html.parser')