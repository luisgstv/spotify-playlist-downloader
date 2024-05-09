from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pytube import Search
from pytube.exceptions import PytubeError
from tkinter import filedialog
import threading
import logging

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
        # Getting the directory to download the musics and the playlist URL
        print('Select a directory to download the musics.')
        self.directory = filedialog.askdirectory()
        self.playlist_url = input('Playlist URL: ')

        self.musics_list = self.get_musics_name(self.playlist_url)

        print('Downloading musics...')
        self.search_musics(self.musics_list)

    def get_musics_name(self, playlist_url):
        # Creating the webdriver
        self.driver = webdriver.Chrome(options=self.options)

        # Going to the page and waiting for it to load
        self.driver.get(playlist_url)

        WebDriverWait(self.driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid="tracklist-row"]'))
        )
        
        # Parsing the page's HTML
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # Getting the music name and the artist name of each music in the playlist
        musics_list = []
        musics = soup.find('div', attrs={'data-testid': 'playlist-tracklist'}).find_all('div', attrs={'data-testid': 'tracklist-row'})
        for music in musics:
            infos = music.find('div', attrs={'aria-colindex': '2'})
            music_name = infos.find('a', attrs={'data-testid': 'internal-track-link'}).find('div', attrs={'data-encore-id': 'text'}).text
            artist_name = infos.find_all('span', attrs={'data-encore-id': 'text'})[-1].text
            musics_list.append(f'{artist_name} - {music_name}')
        
        self.driver.close()
        
        return musics_list

    def search_musics(self, musics_list):
        # Setting control variables
        self.music_counter = 0
        self.total_musics = len(musics_list)

        # Searching each music, getting the first result and creating a Thread to download it
        for music in musics_list:
            search = Search(f'{music} Audio')
            result = search.results[0]
            threading.Thread(target=self.download_musics, args=(music, result)).start()

    def download_musics(self, music, result):
        # Trying to download the music
        try:
            result.streams.get_audio_only().download(output_path=self.directory, filename=f'{music}.mp3')
        except PytubeError:
            print(f'Error downloading music: {music}')
        else:
            self.music_counter += 1
            print(f'Downloaded music {self.music_counter}/{self.total_musics}: {music}')

# Running the application
if __name__ == '__main__':  
    spotify_downloader = SpotifyPlaylistDownloader()
    spotify_downloader.run()