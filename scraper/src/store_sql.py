import sqlite3
import os


def initialize_sql_file(conn, cursor):
    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS artists (
                       artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL,
                       );
                   """
    )

    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS descriptors (
                       descriptor_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       descriptor TEXT NOT NULL UNIQUE
                       );
                   """
    )
    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS genres (
                       genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT NOT NULL UNIQUE
                       );
                   """
    )

    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS albums (
                       album_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       album_name TEXT NOT NULL,
                       release_date TEXT,
                       average rating FLOAT,
                       rating_count INTEGER,
                       review_count INTEGER,
                       FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
                       )
                   """
    )

    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS album_genre (
                       artist_id INTEGER,
                       genre_id INTEGER,
                       FOREIGN KEY (album_id) REFERENCES albums(album_id),
                       FOREIGN KEY (genre_id) REFERENCES genres(genre_id),
                       PRIMARY KEY (album_id, genre_id)
                       )
                   """
    )
    cursor.execute(
        """
                   CREATE TABLE IF NOT EXISTS album_descriptor (
                       artist_id INTEGER,
                       descriptor_id INTEGER,
                       FOREIGN KEY (album_id) REFERENCES albums(album_id),
                       FOREIGN KEY (descriptor_id) REFERENCES descriptor(descriptor_id),
                       PRIMARY KEY (album_id, descriptor_id)
                       )
                   """
    )
    conn.commit()


def insert_genre(cursor, genre_name):
    cursor.execute("SELECT genre_id FROM genres WHERE name = ?", (genre_name,))
    result = cursor.fetchone()
    if result:
        return result[0]

    cursor.execute("INSERT INTO genres (name) VALUES (?)", (genre_name,))
    return cursor.lastrowid


def insert_descriptor(cursor, descriptor_text):
    cursor.execute(
        "SELECT descriptor_id FROM descriptors WHERE descriptor = ?", (descriptor_text,)
    )
    result = cursor.fetchone()
    if result:
        return result[0]

    cursor.execute(
        "INSERT INTO descriptors (descriptor) VALUES (?)", (descriptor_text,)
    )
    return cursor.lastrowid


def insert_artist(cursor, artist_name):
    cursor.execute("SELECT artist_id from WHERE name = ?", (artist_name,))
    result = cursor.fetchone()
    if result:
        return result[0]
    cursor.execute("INSERT INTO artists (name) VALUES (?)", (artist_name))


def insert_album(cursor, album_info, artist_id):
    cursor.execute(
        """
        INSERT INTO albums (album_name, artist_id, release_date, average_rating, rating_count, review_count)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (
            album_info["Album-Name"],
            artist_id,
            album_info["Date"],
            album_info["Score"],
            album_info["Ratings"],
            album_info["Reviews"],
        ),
    )
    return cursor.lastrowid


def link_album_to_genres(cursor, album_id, genres):
    for genre_name in genres:
        genre_id = insert_genre(cursor, genre_name)
        cursor.execute(
            "INSERT INTO album_genre (album_id, genre_id) VALUES (?, ?)",
            (album_id, genre_id),
        )


def link_album_to_descriptors(cursor, album_id, descriptors):
    for descriptor_text in descriptors:
        descriptor_id = insert_descriptor(cursor, descriptor_text)
        cursor.execute(
            "INSERT INTO album_descriptor (album_id, descriptor_id) VALUES (?, ?)",
            (album_id, descriptor_id),
        )


def add_albums_to_sql(albums_list, sqlite_file="output.db"):
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()

    initialize_sql_file(conn, cursor)

    for album in albums_list:
        try:
            artist_id = insert_artist(cursor, album["Artist"])
            album_id = insert_album(cursor, album, artist_id)
            link_album_to_genres(
                cursor, album_id, album["Genres"] + album["Secondary-Genres"]
            )
            link_album_to_descriptors(cursor, album_id, album["Descriptors"])

            conn.commit()
        except Exception as e:
            print(f"Exception occured: {e}")
            conn.rollback()
    conn.close()
