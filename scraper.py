
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests

def get_midi_files(composer_url):
    vid_dict = {}
    browser.get(composer_url)
    try:
        items_block = browser.find_element_by_id('items')

        pieces = items_block.find_elements_by_class_name('ytd-playlist-panel-renderer')
        for vid in playlist:
            title = vid.text
            vid_panel = vid.find_element_by_class_name('ytd-playlist-panel-video-renderer')
            href = vid_panel.get_attribute('href')
            vid_dict[title] = href
    except:
        print(f'unable to get data from {playlist_url}')

def is_200_code(page):
    if page.status_code != 200:
        print(page.status_code)
        return False
    else:
        return True


def get_midi_with_bs(composer_url):
    page = requests.get(composer_url)
    if is_200_code(page):
        soup = bs(page.content, 'html_parser')
        tags = soup.find_all('tr', width=100)
