from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import codecs
import re

from webdriver_manager.chrome import ChromeDriverManager

def main():
    fanduel_url = input('Enter the Fanduel url: ')
    mgm_url = input('Enter the BetMGM url: ')
    # draftkings_url = input('Enter the DraftKings url: ')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    fanduel_html = get_page_html(driver, fanduel_url)
    mgm_html = get_page_html(driver, mgm_url)

    match_odds = {}

    get_fanduel_matches(fanduel_html, match_odds)
    get_mgm_matches(mgm_html, match_odds)
    print(match_odds)
    # print(match_odds)
    # draftkings_html = get_page_html(driver, draftkings_url)
    driver.quit()

def get_fanduel_matches(fanduel_html, match_odds):
    soup = BeautifulSoup(fanduel_html, 'html.parser')
    f = open('newfile.txt', 'w')
    f.write(soup.prettify())
    f.close()
    list = soup.find_all('ul')
    all_matches = None
    for item in list:
        if 'Upcoming' in item.text:
            all_matches = item
            break

    for match in all_matches:
        is_live = match.find(attrs={'aria-label': 'live event'})
        spans = match.find_all('span')

        if not spans or is_live: #if match has started or is not a match
            continue
        is_doubles = '/' in spans[0].text
        if is_doubles:
            continue

        player1, player2 = spans[0].text, spans[1].text
        player1_odds, player2_odds = int(spans[2].text), int(spans[3].text)
        
        if player2 > player1:
            player1, player2 = player2, player1
            player1_odds, player2_odds = player2_odds, player1_odds
        hash = hash_match(player1, player2)
        match_odds[hash] = {}
        match_odds[hash]['p1_odds'] = [player1_odds]
        match_odds[hash]['p2_odds'] = [player2_odds]
    
def get_mgm_matches(mgm_html, match_odds):
    soup = BeautifulSoup(mgm_html, 'html.parser')
    all_matches = soup.select('ms-event.grid-event')
    for match in all_matches:
        is_live = match.select('i.live-icon')
        if is_live:
            continue
        players = match.select('div.participant')
        player1, player2 = players[0].find(text=True, recursive=False), players[1].find(text=True, recursive=False)
        player1, player2 = player1.strip(), player2.strip() # remove leading whitespace
        
        odds = match.find_all('ms-font-resizer')
        player1_odds, player2_odds = int(odds[0].text), int(odds[1].text)

        if player2 > player1:
            player1, player2 = player2, player1
            player1_odds, player2_odds = player2_odds, player1_odds

        hash = hash_match(player1, player2)
        match_odds[hash]['p1_odds'].append(player1_odds)
        match_odds[hash]['p2_odds'].append(player2_odds)
        

# def get_draftkings_matches(draftkings_html, match_odds):
#     soup = BeautifulSoup(draftkings_html, 'html.parser')

def get_page_html(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout=15).until(EC.url_to_be(url))
    curr_url = driver.current_url
    page_source = None
    if curr_url == url:
        page_source = driver.page_source

    return page_source

def hash_match(player1, player2):
    return player1 + '/' + player2

if __name__ == '__main__':
    main()