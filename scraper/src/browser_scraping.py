from logging import exception
import argparse
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

# Replace SAVEDIR and PROXY_PORT with your information or use environment variables
SAVEDIR = "SAVEDIR"
global save_path
PROXY_PORT = "PORT"
GENRES = [
    "ambient",
    "classical-music",
    "hip-hop",
    "industrial-and-noise",
    "blues",
    "country",
    "dance",
    "electronic",
    "folk",
    "jazz",
    "metal",
    "new-age",
    "pop",
    "psychedelia",
    "punk",
    "randb",
    "rock",
    "singer-songwriter",
    "spoken-word",
]


def write_html_file(year, contents, page):
    global save_path
    filename = f"{year}+{page}.html"
    combined_path = os.path.join(save_path, filename)
    try:
        with open(combined_path, "w") as file:
            file.write(contents)
    except FileNotFoundError:
        print("Failed to write to file")


def create_url(year, page, genre):
    return f"https://rateyourmusic.com/charts/top/album/{year}/g:{genre}/{page}/"


def get_final_page(driver, year, genre):
    try:
        driver.get(create_url(year, 1, genre))
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "header_logo"))
        )
    except TimeoutException:
        return (False, None)

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, "html.parser")

    pagination_div = soup.find("div", class_="ui_pagination")

    num_pages = pagination_div["data-num-pages"] if pagination_div else "0"
    return True, int(num_pages) + 1


def initialize_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    options.add_argument(f"--proxy-server=http://{PROXY_PORT}")
    driver = webdriver.Chrome(options=options)
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver


def save_page(driver, page, year, genre):
    url = create_url(year, page, genre)
    attempts = 1
    while True:
        try:
            driver.get(url)
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "header_logo"))
            )
            break
        except TimeoutException:
            if attempts > 1:
                try:
                    if driver:
                        driver.quit()
                    return [year, page]
                except:
                    return [year, page]
            else:
                attempts += 1

    while driver.execute_script("return document.readyState") != "complete":
        time.sleep(0.5)
    html_content = driver.page_source
    write_html_file(year, html_content, page)
    print(f"Genre: {genre}, Year: {year}, Page:{page}")


def get_html_until_break(initial_year, initial_page, genre):
    start_time = time.time()
    for year in range(initial_year, 2024):
        if year == initial_year:
            start_page = initial_page
        else:
            start_page = 1
        attempts = 1
        driver = initialize_webdriver()
        while attempts < 5:
            try:
                success, end_page = get_final_page(driver, year, genre)
                break
            except:
                if driver:
                    driver.refresh()
                time.sleep(5)
                attempts += 1
        else:
            raise Exception("Could not open webpage")
        if not success:
            return (False, [year, start_page], start_time)

        for page in range(start_page, end_page):
            attempts = 1
            while attempts < 5:
                try:
                    result = save_page(driver, page, year, genre)
                    break
                except Exception as e:
                    print(f"Exception {e}, running again attempt number: {attempts}")
                    attempts += 1
            else:
                raise Exception("Could not call save_page function")
            if result:
                return (False, result, start_time)
        attempts2 = 1
        while attempts2 < 5:
            try:
                if driver:
                    driver.quit()
                break
            except Exception as e:
                print(f"Exception: {e}")
                attempts2 += 1
        else:
            raise Exception("Could not close driver")
    return (True, [2024, 1], start_time)


def run_driver(start_genre_index, initial_genre_year_start, initial_genre_page_start):
    for i in range(start_genre_index, len(GENRES)):
        if i == start_genre_index:
            year_start = initial_genre_year_start
            page_start = initial_genre_page_start
        else:
            year_start = 1960
            page_start = 1
        handle_save_path(GENRES[i])
        while year_start < 2024:
            success, array, start_time = get_html_until_break(
                year_start, page_start, GENRES[i]
            )
            if success:
                break
            year_start = array[0]
            page_start = array[1]
            print(year_start)
            print(page_start)
            print(f"{GENRES[i]} - {i}")
            while time.time() - start_time < 120:
                time.sleep(1)


def get_htmls(initial_year, initial_page, genre):
    driver = initialize_webdriver()
    start_time = time.time()
    for year in range(initial_year, 2024):
        if year == initial_year:
            start_page = initial_page
        else:
            start_page = 1
        end_page = get_final_page(driver, year, genre)
        for page in range(start_page, end_page):
            result = save_page(driver, page, year, genre)
            if result:
                return (result, start_time)
    return ([2024, 1], start_time)


def handle_save_path(genre):
    global save_path
    path = f"{SAVEDIR}{genre}/"
    if not os.path.exists(f"{SAVEDIR}/{genre}/"):
        os.chdir(SAVEDIR)
        os.makedirs(genre)
    save_path = path


def main():
    parser = argparse.ArgumentParser(description="Webscraper")
    parser.add_argument("start_genre_index", help="Initial Index of Genre", type=int)
    parser.add_argument("year_start_initial", help="Initial Year of Genre", type=int)
    parser.add_argument("page_start_initial", help="Initial Page of Genre", type=int)

    args = parser.parse_args()
    run_driver(args.start_genre_index, args.year_start_initial, args.page_start_initial)


if __name__ == "__main__":
    main()
