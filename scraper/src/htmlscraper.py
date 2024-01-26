from bs4 import BeautifulSoup
import argparse
from albumscraper import AlbumScraper
import os


class HtmlScraper:
    def __init__(self, file):
        self.file = file

    def scrape_html_file(self):
        # print(filepath)

        result = []
        with open(self.file, "r") as file:
            if not file:
                raise FileNotFoundError
            string = file.read()
            html_soup = BeautifulSoup(string, "html.parser")
            album_divs = html_soup.select("div.page_section_charts_item_wrapper.anchor")
            counter = 0
            for album_div in album_divs:
                # print(counter)
                counter += 1
                album = AlbumScraper(album_div)
                album_data = album.get_album_data()
                result.append(album_data)

        return result

    def walk_directory(self):
        albums = []
        for dirpath, dirnames, filenames in os.walk(self.directory):
            for filename in filenames:
                if filename.endswith(".html"):
                    page_albums = self.scrape_html_file(os.path.join(dirpath, filename))
                    albums = albums + page_albums
        # print(f"albums: {albums}")
        return albums
