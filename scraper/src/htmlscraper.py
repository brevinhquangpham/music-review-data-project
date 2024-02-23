from bs4 import BeautifulSoup
from albumscraper import AlbumScraper
import os


def scrape_html_file(filepath):

    result = []
    with open(filepath, "r") as file:
        if not file:
            raise FileNotFoundError
        string = file.read()
        html_soup = BeautifulSoup(string, "html.parser")
        album_divs = html_soup.select("div.page_section_charts_item_wrapper.anchor")
        counter = 0
        for album_div in album_divs:
            counter += 1
            album = AlbumScraper(album_div)
            album_data = album.get_album_data()
            result.append(album_data)

    return result


def walk_directory(directory):
    albums = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".html"):
                page_albums = scrape_html_file(os.path.join(dirpath, filename))
                albums = albums + page_albums
    return albums
