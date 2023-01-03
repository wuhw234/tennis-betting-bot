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
        hard_elo = elo - 25 if entries[5].text == '-' else float(entries[5].text)
        clay_elo = elo - 25 if entries[6].text == '-' else float(entries[6].text)
        grass_elo = elo - 25 if entries[7].text == '-' else float(entries[7].text)

        elo_dict[name] = {}
        elo_dict[name]['elo'] = elo
        elo_dict[name]['hard_elo'] = hard_elo
        elo_dict[name]['clay_elo'] = clay_elo
        elo_dict[name]['grass_elo'] = grass_elo
    
    return elo_dict

if __name__ == "__main__":
    get_elo('w')

    