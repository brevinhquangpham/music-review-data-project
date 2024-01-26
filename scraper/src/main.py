import os
from store_sql import add_albums_to_sql
from htmlscraper import HtmlScraper
import argparse
import time
import progressbar


def walk_directory(directory, output_db):
    for dirpath, dirnames, filenames in os.walk(directory):
        bar = progressbar.ProgressBar(max_value=len(filenames))
        counter = 0
        for filename in filenames:
            bar.update(counter)
            counter += 1
            if filename.endswith(".html"):
                # print(f"Adding albums to sql {filename}")
                # print("-----------------------------")
                scraper = HtmlScraper(os.path.join(dirpath, filename))
                page_albums = scraper.scrape_html_file()
                add_albums_to_sql(page_albums, output_db)
        bar.finish()


def main():
    parser = argparse.ArgumentParser(
        description="Scrape rym html and save to SQL database"
    )
    parser.add_argument("input")
    parser.add_argument("output", default="output.sql")

    args = parser.parse_args()
    input = os.path.abspath(args.input)
    output = os.path.abspath(args.output)
    walk_directory(input, output)


if __name__ == "__main__":
    main()
