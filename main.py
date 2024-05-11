from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pytube import Search
from pytube.exceptions import PytubeError
from tkinter import filedialog
import threading
import logging
import time

class SpotifyPlaylistDownloader:
    def __init__(self):
        # Creating the ChromeOptions
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--log-level=3')

        # Removing the errors from pytube
        pytube_logger = logging.getLogger('pytube')
        pytube_logger.setLevel(logging.ERROR)

    def run(self):
        # Getting the directory to download the songs, and the playlist URL
        print('Select a directory to download the songs.')
        self.directory = filedialog.askdirectory()
        self.playlist_url = input('Playlist URL: ')

        self.song_list = self.get_songs_name(self.playlist_url)

        print('Downloading songs...')
        self.search_songs(self.song_list)

    def get_songs_name(self, playlist_url):
        # Creating the webdriver
        self.driver = webdriver.Chrome(options=self.options)

        # Going to the page and waiting for it to load
        self.driver.get(playlist_url)

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.contentSpacing div div span.encore-text-body-small'))
        )

        # Getting a scrollable element to scroll the page
        self.scrollable_element = self.driver.find_element(By.TAG_NAME, 'main')

        self.scrollable_element.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        self.scrollable_element.send_keys(Keys.PAGE_UP)

        # Getting the number of total songs
        self.total_songs = int(self.driver.find_element(By.XPATH, '//div[contains(@class, "contentSpacing")]//span[contains(text(), "song")]').text.split(' ')[0])
        print(self.total_songs)

        song_dict = {}
        while len(song_dict) < self.total_songs:
            time.sleep(1.5)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            songs = soup.find('div', attrs={'data-testid': 'playlist-tracklist'}).find_all('div', attrs={'data-testid': 'tracklist-row'})
            for song in songs:
                infos = song.find('div', attrs={'aria-colindex': '2'})
                index = song.find('div', attrs={'aria-colindex': '1'}).find('span').text
                song_name = infos.find('a', attrs={'data-testid': 'internal-track-link'}).find('div', attrs={'data-encore-id': 'text'}).text
                artist_name = infos.find_all('span', attrs={'data-encore-id': 'text'})[-1].text
                song_dict[index] = f'{artist_name} - {song_name}'
            print(len(song_dict))
            self.scrollable_element.send_keys(Keys.PAGE_DOWN * 2)
        
        song_list = list(song_dict.values())
        
        self.driver.close()
        
        return song_list

    def search_songs(self, song_list):
        # Setting control variables
        self.song_counter = 0
        self.total_songs = len(song_list)

        # Searching each song, getting the first result and creating a Thread to download it
        for song in song_list:
            search = Search(f'{song} Audio')
            result = search.results[0]
            threading.Thread(target=self.download_songs, args=(song, result)).start()

    def download_songs(self, song, result):
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '>', '<', '|']
        for char in invalid_chars:
            if char in song:
                song = song.replace(char, ' ')
        # Trying to download the song
        try:
            result.streams.get_audio_only().download(output_path=self.directory, filename=f'{song}.mp3')
        except PytubeError:
            print(f'Error downloading song: {song}')
        else:
            self.song_counter += 1
            print(f'{self.song_counter}/{self.total_songs} - Successfully downloaded song: {song}')

# Running the application
if __name__ == '__main__':  
    spotify_downloader = SpotifyPlaylistDownloader()
    spotify_downloader.run()