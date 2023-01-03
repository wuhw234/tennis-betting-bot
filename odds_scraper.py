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
    betmgm_url = input('Enter the BetMGM url: ')
    draftkings_url = input('Enter the DraftKings url: ')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    fanduel_html = get_page_html(driver, fanduel_url)
    matches_dict = {}

    get_fanduel_matches(fanduel_html, matches_dict)
    # betmgm_html = get_page_html(driver, betmgm_url)
    # draftkings_html = get_page_html(driver, draftkings_url)
    driver.quit()

def get_fanduel_matches(fanduel_html, matches_dict):
    soup = BeautifulSoup(fanduel_html, 'html.parser')
    list = soup.find_all('ul')[3]
    all_matches = list.select('div.af.ag.ah.ai.ct.cu.aj.fn.s.df.hp.hq.bk.h.i.j.al.l.m.am.o.an.q.ao')

    for match in all_matches:
        is_live = match.find(attrs={'aria-label': 'live event'})
        if is_live:
            continue
        players = match.select('span.ae.aj.ie.if.ig.ih.hr.hs.ht.hw.ii.s.ff.ec.ij.h.i.j.al.l.m.am.o.an.q.ao.br')
        player1, player2 = players[0].text, players[1].text
        if '/' in player1: # ignore doubles matches
            continue

        odds = match.find_all(attrs={'role': 'button'})
        player1_odds, player2_odds = odds[0].text, odds[1].text

        hash = hash_match(player1, player2)
        if hash not in matches_dict:
            matches_dict[hash] = {}
        matches_dict[hash]['p1_name'] = player1
        matches_dict[hash]['p2_name'] = player2
        matches_dict[hash]['fanduel_p1_odds'] = player1_odds
        matches_dict[hash]['fanduel_p2_odds'] = player2_odds
    
# def get_draftkings_matches(draftkings_html, matches_dict):
#     soup = BeautifulSoup(draftkings_html, 'html.parser')

def get_page_html(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout=10).until(EC.url_to_be(url))
    curr_url = driver.current_url
    page_source = None
    if curr_url == url:
        page_source = driver.page_source

    return page_source

def hash_match(player1, player2):
    if player1 > player2:
        return player1 + player2
    else:
        return player2 + player1

if __name__ == '__main__':
    main()