import sqlite3
from bs4 import BeautifulSoup


def convert_month_to_number(word_month):
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    for i in range(0, len(months)):
        if word_month == months[i]:
            return i + 1

    raise Exception("Invalid Month Error")


def convert_date_to_numeric(date):
    date_split = date.split("")
    year = 2000
    month = 1
    day = 1
    for i in range(0, len(date_split)):
        current_index = len(date_split) - (i + 1)
        if i == 0:
            year = date_split[current_index]
        elif i == 1:
            numeric_month = convert_month_to_number(date_split[current_index])
            month = numeric_month
        elif i == 2:
            day = date_split[current_index]

    return f"{month}/{day}/{year}"


def get_text_from_links(div, class_name):
    result = []
    links = div.find_all("a", class_=class_name)
    for link in links:
        link_text = link.get_text()
        result.append(link_text)
    return result


def get_text_from_nested_span(parent, class_name):
    span = parent.find("span", class_=class_name)
    if span:
        nested_span = span.find("span", class_="full")
        if nested_span:
            return nested_span.get_text()
    return None  # or an appropriate default value


def get_descriptors(descriptor_div):
    return get_text_from_links(descriptor_div, "comma_separated")


def get_genres(genre_div):
    return get_text_from_links(genre_div, "genre comma_separated")


def get_album_data(album):
    album_title_div = album.find("div", class_="page_charts_section_charts_item_title")
    album_title = album_title_div.find("span", class_="ui_name_locale_original").text
    artist_name_a = album.find("a", class_="artist")
    artist_name = artist_name_a.find("span", class_="ui_name_locale_original").text
    genre_div = album.find(
        "div", class_="page_charts_section_charts_item_genres_primary"
    )
    genre2_div = album.find(
        "div", class_="page_charts_section_charts_item_genres_secondary"
    )
    descriptor_div = album.find(
        "div", class_="page_charts_section_charts_item_genre_descriptors"
    )
    average_score = album.find(
        "span", class_="page_charts_section_charts_item_details_average_num"
    ).text

    date = album.find("div", class_="page_charts_section_charts_item_date")

    ratings = get_text_from_nested_span(
        album, "page_charts_section_charts_item_details_ratings"
    )
    reviews = get_text_from_nested_span(
        album, "page_charts_section_charts_item_details_reviews"
    )
    result = {
        "Album-Name": album_title,
        "Artist": artist_name,
        "Genres": get_genres(genre_div),
        "Secondary-Genres": get_genres(genre2_div),
        "Descriptors": get_descriptors(descriptor_div),
        "Score": average_score,
        "Ratings": ratings,
        "Reviews": reviews,
    }
    return result


def get_data_from_html(html_content):
    result = []
    page = BeautifulSoup(html_content, "html.parser")
    listings = page.find_all("div", class_="page_section_charts_item_wrapper  anchor")
    for album in listings:
        result.append(get_album_data(album))
