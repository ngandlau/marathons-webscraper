from bs4 import BeautifulSoup
import requests
import pandas as pd

# runnersworld website 
url = 'https://larasch.de/eventkarte?sport=Laufen&date=2022-05-25&days=42'
html = requests.get(url).content
soup = BeautifulSoup(html, features="lxml")


