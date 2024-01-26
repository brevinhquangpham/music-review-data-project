import sqlite3
import pandas as pd

# Connect to your SQLite database
conn = sqlite3.connect("output.db")
cursor = conn.cursor()

# SQL query to join tables and retrieve the desired data
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
# Fetch data from the joined tables and create a DataFrame
df = pd.read_sql_query(query, conn)

# Save the DataFrame as a CSV file
df.to_csv("combined_data.csv", index=False)

# Close the database connection
conn.close()
