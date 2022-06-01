from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

def extract_page_urls(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")

    nav = soup.find('div', class_='navigation')
    max_page = max([int(a.text) for a in nav.find_all('a')])

    pages = [url]
    for i in range(2, max_page+1):
        url = f'http://www.volkslauf-ergebnisse.de/{i}/date/'
        pages.append(url)
    return pages

def extract_run_urls(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, features="lxml")
    run_urls = []
    for run in soup.find_all('div', class_='lauf_eintrag'):
        urls = [main_url + a['href'] for a in run.find_all('a', href=True) if a['href'].startswith('/list')]
        run_urls += urls 
    run_urls
    return run_urls

def extract_name(soup, remove_digits=False):
        name = soup.find('h1', class_='topic').text
        name = name.strip()

        if remove_digits:
                # remove digits in front of string
                # Example: "35. Hördter Waldlauf" -> Hördter Waldlauf
                name = re.sub(r'\d*\.', '', name).strip()
        return name

def extract_infos(soup):
        location, date, distance, n_runners = soup.find('div', class_='sub_text').text.split(' | ')
        n_runners = [int(n) for n in re.findall(r'\d+', n_runners)][0]
        distance = float(distance.replace(' km', ''))
        return location, date, distance, n_runners


# MAIN LOOP
main_url =  'http://www.volkslauf-ergebnisse.de/'
page_urls = extract_page_urls(main_url)

for i, page in enumerate(page_urls):
    data = []
    run_urls = extract_run_urls(page)
    for run in run_urls:
        response = requests.get(run)
        soup = BeautifulSoup(response.content, features="lxml")

        name = extract_name(soup)
        location, date, distance, n_runners = extract_infos(soup)
        row = {
                'name_of_run': name,
                'location': location,
                'date': date,
                'distance_km': distance,
                'n_runners': n_runners
        }
        data.append(row)
    df = pd.DataFrame(data)
    if i == 0:
        df.to_csv("data/volkslaufergebnisse_runs.csv", mode='a', index=False, encoding="utf-8-sig")
    else:
        df.to_csv("data/volkslaufergebnisse_runs.csv", mode='a', index=False, encoding="utf-8-sig", header=False)


    



