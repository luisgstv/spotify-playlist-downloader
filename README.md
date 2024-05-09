# Spotify Playlist Downloader

This project consists of an automation script that includes a Spotify web scraper, which scrapes all the songs in a playlist, and a YouTube Downloader that searches for and downloads each song, saving them in a selected directory.

## Tools and Modules

- This project uses **Selenium** and **BeautifulSoup4** to scrape each song from the Spotify playlist.
- The **Pytube** module is used to search for and download each song scraped from Spotify.
- The **Threading** module is used to download the songs in separate threads for faster execution.

## How it works

When you run the program, you'll need to select a directory for downloading the songs and enter the Spotify playlist URL in the terminal. The Selenium WebDriver will then open the provided [Spotify] URL and, once the page is fully loaded, scrape all the songs in the playlist, capturing both the song names and the artists' names. After the scraping process is complete, it will search for each song on [YouTube] using the Pytube module and download the first result into the selected directory in the .mp3 format.

## How to use

To use this project, you will need to follow these steps:

1. Clone this repository using the following command:

```
    git clone https://github.com/luisgstv/airbnb-webscraper.git
```

2. Install the required modules using the following command:

```
    pip install -r requirements.txt
```

3. Once you run the script, select a directory to download the songs and enter the Spotify playlist you want to scrape.
