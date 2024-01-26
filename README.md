# Project overview

This project aims to scrape and analyze music review data from Rate Your Music (RYM), a community-driven music database and review site. By examining user reviews and ratings, we seek to uncover insights into music trends, genre popularity, and factors contributing to an album's acclaim or criticism.

# Tools and Technologies
- Selenium
- Selenium-Stealth
- Pandas
- Sqlite3
- BeautifulSoup
- progressbar2

# Data Source

The data for this project is scraped from Rate Your Music, specifically focusing on album reviews, ratings, and metadata.

# How to use
- To gain access to the data, one must first scrape the website
- This version of the scraper scrapes RYM's charts so that an ample amount of data can be scraped before an ip ban
- Edit `src/browser_scraper` and replace "SAVEDIR" and "PROXYPORT" with values or environment variables
- **Rotating Proxies Recommended** - *RYM has an extremely sensitive firewall such that vpns typically get banned*
- Call: `python run.py --mode browser_scraper <index_of_genre> <initial_year> <initial_page>`
    - To see the list of available genres view the genres list in `src/browser_scraper.py`
    - This will scrape through chart pages of the given genre and save the htmls to SAVEDIR
- To scrape the html data call `python run.py --mode main <dir of html files> <output database file>`
- This command will scrape the html file into a sqlite3 file.
- 
# Features Scraped
- Album title and artist
- Album release year and genres
- Average user ratings
- User rating number
- Album descriptors
