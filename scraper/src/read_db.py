import sqlite3
import pandas as pd


# Temporary to create csv file
def clean_data(df):
    # Fill missing values
    df["Album_Name"].fillna("Unknown", inplace=True)
    df["Artist_Name"].fillna("Unknown", inplace=True)
    df["Release_Date"] = pd.to_datetime(df["Release_Date"]).dt.strftime(
        "%Y-%m-%d"
    )  # Standardize date format
    df["Genres"].fillna("None", inplace=True)
    df["Descriptors"].fillna("None", inplace=True)
    df["Average_Rating"].fillna(
        df["Average_Rating"].mean(), inplace=True
    )  # Fill with mean or choose another strategy
    df["Rating_Count"].fillna(0, inplace=True)
    df["Review_Count"].fillna(0, inplace=True)

    # Convert numeric columns to appropriate types if not already
    df["Average_Rating"] = df["Average_Rating"].astype(float)
    df["Rating_Count"] = df["Rating_Count"].astype(int)
    df["Review_Count"] = df["Review_Count"].astype(int)

    df["Genres"] = df["Genres"].apply(lambda x: x.split(",") if x else [])
    df["Descriptors"] = df["Descriptors"].apply(lambda x: x.split(",") if x else [])

    subset_columns = [
        "Album_Name",
        "Artist_Name",
        "Release_Date",
        "Average_Rating",
        "Rating_Count",
        "Review_Count",
    ]
    df.drop_duplicates(subset=subset_columns, inplace=True)

    # Additional cleaning tasks as needed...

    return df


def main():
    conn = sqlite3.connect("output.db")
    cursor = conn.cursor()

    query = """
        SELECT
            albums.album_name AS Album_Name,
            artists.name AS Artist_Name,
            albums.release_date AS Release_Date,
            GROUP_CONCAT(DISTINCT genres.name) AS Genres,
            GROUP_CONCAT(DISTINCT descriptors.descriptor) AS Descriptors,
            albums.average_rating AS Average_Rating,
            albums.rating_count AS Rating_Count,
            albums.review_count AS Review_Count
        FROM albums
        LEFT JOIN artists ON albums.artist_id = artists.artist_id
        LEFT JOIN album_genre ON albums.album_id = album_genre.album_id
        LEFT JOIN genres ON album_genre.genre_id = genres.genre_id
        LEFT JOIN album_descriptor ON albums.album_id = album_descriptor.album_id
        LEFT JOIN descriptors ON album_descriptor.descriptor_id = descriptors.descriptor_id
        GROUP BY albums.album_id
    """
    df = pd.read_sql_query(query, conn)

    pd.set_option("display.max_rows", None)  # This will allow all rows to be displayed.
    pd.set_option(
        "display.max_columns", None
    )  # This will allow all columns to be displayed.
    pd.set_option(
        "display.width", None
    )  # This will help ensure the display width is not constrained.
    pd.set_option("display.max_colwidth", None)
    df = clean_data(df)
    print(df.head())
    df.to_csv("combined_data.csv", index=False)

    conn.close()
