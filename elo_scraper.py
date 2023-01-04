from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager

from odds_scraper import get_page_html, standardize_name

def get_elo(gender):
    if gender == 'm':
        url = 'http://tennisabstract.com/reports/atp_elo_ratings.html'
    else:
        url = 'http://tennisabstract.com/reports/wta_elo_ratings.html'
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    html = get_page_html(driver, url)

    elo_dict = {}

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'id': 'reportable'})
    table_body = table.find('tbody')
    for row in table_body:
        entries = row.find_all('td')
        name = standardize_name(entries[1].text)
        elo = float(entries[3].text)
        hard_elo = elo - 100 if entries[5].text == '-' else float(entries[5].text)
        clay_elo = elo - 100 if entries[6].text == '-' else float(entries[6].text)
        grass_elo = elo - 100 if entries[7].text == '-' else float(entries[7].text)

        elo_dict[name] = {}
        elo_dict[name]['elo'] = elo
        elo_dict[name]['hard_elo'] = hard_elo
        elo_dict[name]['clay_elo'] = clay_elo
        elo_dict[name]['grass_elo'] = grass_elo

    get_yelo(gender, driver, elo_dict)
    
    return elo_dict

def get_yelo(gender, driver, elo_dict):
    if gender == 'm':
        url = 'http://tennisabstract.com/reports/atp_season_yelo_ratings.html'
    else:
        url = 'http://tennisabstract.com/reports/wta_season_yelo_ratings.html'
    
    html = get_page_html(driver, url)

    soup = BeautifulSoup(html, 'html.parser')

    table = soup.find('table', {'id': 'reportable'})
    table_body = table.find('tbody')
    for row in table_body:
        entries = row.find_all('td')
        name = standardize_name(entries[1].text)
        yelo = float(entries[4].text)
        wins = int(entries[2].text)
        losses = int(entries[3].text)

        if name not in elo_dict:
            continue
        elo_dict[name]['total_matches'] = wins + losses
        elo_dict[name]['yelo'] = yelo

if __name__ == "__main__":
    get_elo('w')

    