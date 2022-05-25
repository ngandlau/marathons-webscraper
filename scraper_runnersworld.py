from bs4 import BeautifulSoup
import requests
import pandas as pd

# runnersworld website 
url = 'https://www.runnersworld.de/volkslaeufe-strassenlaeufe/'
html = requests.get(url).content
soup = BeautifulSoup(html, features="lxml")


# runnersworld contains several pages of runs 
max_page = soup.findAll('a', class_="v-A_-button v-A_-button--medium v-A_-button--mediumgrey")[-1].text
max_page = int(float(max_page.strip()))
pages = []
pages.append(url)
for i in range(int(max_page)):
    url = 'https://www.runnersworld.de/volkslaeufe-strassenlaeufe/?p=' + str(i+1)
    pages.append(url)


# helper functions
def extract_runs_urls(url):
    """Extracts the urls of each run in a webpage"""
    run_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
    
    for x in soup.findAll('a'):
        run_url = x.get('href')
        if run_url is None:
            continue
        if "laufkalender" in run_url:
            if "laufeintragen" in run_url:
                continue
            if run_url == 'https://www.runnersworld.de/laufkalender/':
                continue
            run_urls.append(run_url)    
    return run_urls

# extract infos from each run's individual webpage's 
def extract_name(soup):
    name = soup.find('span', class_='v-A_-headline v-A_-headline__article--alpha').text
    return name

def extract_date(soup):
    date = soup.find('div', class_='v-A_-appointment').find('span').text
    return date

def extract_website(soup):
    website = soup.find('div', class_='v-A_-information v-A_-connection').find('a').text
    return website

def extract_location(soup):
    location = soup.find('div', class_='v-A_-information v-A_-location').find('span').text
    location = location.strip('\n')
    return location

def extract_table(soup):
    table = soup.find('table')

    rows = [] #make list for rows
    for row in table.findAll('tr'):
        list_cells = [] # array for row
        for cell in row.findAll('td'):
            text = cell.text.replace('&nbsp;', '') #replace nonbreaking space
            text = text.strip()
            list_cells.append(text)
        if len(list_cells) > 0:
            rows.append(list_cells)
    return rows

# extract info for each url
for page_url in pages:
    data = []
    run_urls = extract_runs_urls(page_url)
    for url in run_urls:
        html = requests.get(url).content
        soup = BeautifulSoup(html, features="lxml")
        
        name = extract_name(soup)
        date = extract_date(soup)
        website = extract_website(soup)
        location = extract_location(soup)
        run_info = extract_table(soup)

        data_run = {
            'name' : name,
            'date' : date,
            'website' : website,
            'location' : location,
            'run_info' : run_info
        }
        data.append(data_run)
    df = pd.DataFrame(data) 

    # append to csv file
    df.to_csv("data/runnersworld.csv", mode='a', index=False, encoding="utf-8-sig")
