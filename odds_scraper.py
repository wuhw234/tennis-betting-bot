from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager

def get_odds():
    fanduel_url = input('Enter the Fanduel url: ')
    mgm_url = input('Enter the BetMGM url: ')
    draftkings_url = input('Enter the DraftKings url: ')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    fanduel_html = get_page_html(driver, fanduel_url)
    mgm_html = get_mgm_html(driver, mgm_url)
    draftkings_html = get_page_html(driver, draftkings_url)

    match_odds = {}

    get_fanduel_matches(fanduel_html, match_odds)
    get_mgm_matches(mgm_html, match_odds)
    get_draftkings_matches(draftkings_html, match_odds)

    driver.quit()

    return match_odds

def get_fanduel_matches(fanduel_html, match_odds):
    soup = BeautifulSoup(fanduel_html, 'html.parser')
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
        player1, player2 = standardize_name(player1), standardize_name(player2)
        player1_odds, player2_odds = int(spans[2].text), int(spans[3].text)
        
        if player2 > player1:
            player1, player2 = player2, player1
            player1_odds, player2_odds = player2_odds, player1_odds
        hash = hash_match(player1, player2)
        if hash not in match_odds:
            match_odds[hash] = {}
            match_odds[hash]['p1_odds'] = []
            match_odds[hash]['p2_odds'] = []

        match_odds[hash]['p1_odds'].append((player1_odds, 'Fanduel'))
        match_odds[hash]['p2_odds'].append((player2_odds, 'Fanduel'))
    
def get_mgm_matches(mgm_html, match_odds):
    soup = BeautifulSoup(mgm_html, 'html.parser')
    all_matches = soup.select('ms-event.grid-event')

    for match in all_matches:
        is_live = match.select('i.live-icon')
        if is_live:
            continue
        players = match.select('div.participant')
        player1, player2 = players[0].find(text=True, recursive=False), players[1].find(text=True, recursive=False)
        player1, player2 = standardize_name(player1), standardize_name(player2)
        
        odds = match.find_all('ms-font-resizer')
        player1_odds, player2_odds = int(odds[0].text), int(odds[1].text)

        if player2 > player1:
            player1, player2 = player2, player1
            player1_odds, player2_odds = player2_odds, player1_odds

        hash = hash_match(player1, player2)
        if hash not in match_odds:
            match_odds[hash] = {}
            match_odds[hash]['p1_odds'] = []
            match_odds[hash]['p2_odds'] = []

        match_odds[hash]['p1_odds'].append((player1_odds, 'BetMGM'))
        match_odds[hash]['p2_odds'].append((player2_odds, 'BetMGM'))
        

def get_draftkings_matches(draftkings_html, match_odds):
    soup = BeautifulSoup(draftkings_html, 'html.parser')
    all_matches = soup.select('div.sportsbook-event-accordion__children-wrapper')

    for match in all_matches:
        is_live = match.select('span.sportsbook__icon--live')
        if is_live:
            continue
        players = match.select('span.sportsbook-outcome-cell__label')
        player1, player2 = players[0].text, players[1].text
        player1, player2 = standardize_name(player1), standardize_name(player2)
        
        odds = match.select('span.sportsbook-odds')
        player1_odds, player2_odds = odds[0].text, odds[1].text
        if player1_odds[0] != '+':
            player1_odds = int(swap_minus(player1_odds))
        if player2_odds[0] != '+':
            player2_odds = int(swap_minus(player2_odds))
        
        if player2 > player1:
            player1, player2 = player2, player1
            player1_odds, player2_odds = player2_odds, player1_odds

        hash = hash_match(player1, player2)
        if hash not in match_odds:
            match_odds[hash] = {}
            match_odds[hash]['p1_odds'] = []
            match_odds[hash]['p2_odds'] = []

        match_odds[hash]['p1_odds'].append((player1_odds, 'BetMGM'))
        match_odds[hash]['p2_odds'].append((player2_odds, 'BetMGM'))

        
def get_page_html(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout=15).until(EC.url_to_be(url))
    curr_url = driver.current_url
    page_source = None
    if curr_url == url:
        page_source = driver.page_source

    return page_source

def get_mgm_html(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout=15).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-group')))

    return driver.page_source

def standardize_name(player):
    player.strip()
    player_arr = player.split()
    return player_arr[0] + " " + player_arr[-1]

def hash_match(player1, player2):
    return player1 + '/' + player2

def swap_minus(player_odds):
    player_odds = '-' + player_odds[1:]
    return player_odds

if __name__ == '__main__':
    get_odds()