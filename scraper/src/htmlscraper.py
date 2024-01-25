from bs4 import BeautifulSoup
import argparse
from src.albumscraper import AlbumScraper
import os


class HtmlScraper:
    def __init__(self, directory):
        self.directory = directory

    def scrape_html_file(self, filepath):
        result = []
        with open(filepath, "r") as file:
            if not file:
                raise FileNotFoundError
            html_soup = BeautifulSoup(file, "html.parser")
            album_divs = html_soup.find_all(
                "div", class_="page_section_charts_item_wrapper  anchor"
            )

            for album_div in album_divs:
                album = AlbumScraper(album_div)
                album_data = album.get_album_data()
                result.append(album_data)

        return result

    def walk_directory(self):
        albums = []
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                if filename.endswith(".html"):
                    page_albums = self.scrape_html_file(os.path.join(dirpath, filename))
                    albums = albums + page_albums
        return albums
