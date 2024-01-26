from bs4 import BeautifulSoup


def treat_ratings_and_reviews(string):
    subject = str(string).strip() or "0"
    subject = subject.replace(",", "")
    return int(subject)


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
    date_split = date.split(" ")
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
    return None


def get_descriptors(descriptor_div):
    result = []
    if not descriptor_div:
        return None
    comma_separated_spans = descriptor_div.find_all("span", class_="comma_separated")
    for span in comma_separated_spans:
        result.append(span.text)

    return result


def get_genres(genre_div):
    if not genre_div:
        return None
    return get_text_from_links(genre_div, "genre comma_separated")


class AlbumScraper:
    def __init__(self, album_div):
        self.album = album_div

    def get_album_data(self):
        album_title_div = self.album.find(
            "div", class_="page_charts_section_charts_item_title"
        )
        album_title = album_title_div.find(
            "span", class_="ui_name_locale_original"
        ).text
        artist_name_a = self.album.find("a", class_="artist")

        if artist_name_a:
            artist_name_span = artist_name_a.find(
                "span", class_="ui_name_locale_original"
            ) or artist_name_a.find("span", class_="ui_name_locale")
            artist_name = (
                artist_name_span.text if artist_name_span else "Various Artists"
            )
        else:
            artist_name = "Various Artists"
        genre_div = self.album.find(
            "div", class_="page_charts_section_charts_item_genres_primary"
        )
        genre2_div = self.album.find(
            "div", class_="page_charts_section_charts_item_genres_secondary"
        )
        descriptor_div = self.album.find(
            "div", class_="page_charts_section_charts_item_genre_descriptors"
        )
        average_score = self.album.find(
            "span", class_="page_charts_section_charts_item_details_average_num"
        ).text
        if average_score == "":
            average_score = "0"

        date_div = self.album.find("div", class_="page_charts_section_charts_item_date")
        date_span = date_div.find("span")
        date_numeric = convert_date_to_numeric(date_span.text)

        ratings_text = get_text_from_nested_span(
            self.album, "page_charts_section_charts_item_details_ratings"
        )
        reviews_text = get_text_from_nested_span(
            self.album, "page_charts_section_charts_item_details_reviews"
        )
        ratings = treat_ratings_and_reviews(ratings_text)
        reviews = treat_ratings_and_reviews(reviews_text)
        # print(album_title)
        # print(get_genres(genre_div))
        result = {
            "Album-Name": album_title,
            "Artist": artist_name,
            "Genres": get_genres(genre_div),
            "Secondary-Genres": get_genres(genre2_div),
            "Descriptors": get_descriptors(descriptor_div),
            "Score": float(average_score),
            "Ratings": ratings,
            "Reviews": reviews,
            "Date": date_numeric,
        }
        return result
