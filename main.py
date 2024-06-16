from scr.crawler import Crawler
from scr.mongodb import client
import datetime

# Parameters
news_url = 'https://finance.yahoo.com/topic/latest-news/'
max_items = 5

# Get the news html
crawler = Crawler()

news_html = crawler.get_news_html(news_url)

# Get the soup from the news
news_soup = crawler.get_news_soup(raw_html = news_html)

# Get the items news from the search
news_items = crawler.get_news_items_html(soup=news_soup, max_index=max_items)

# Get a list of data from each item
items_data = crawler.get_news_data(html_raw_list = news_items)

# Acess the database
db_connection = client['db_crawler_headline']

# Acess the collection
collection = db_connection.get_collection('crawler_headline')

# Insert the data in collection
data = collection.insert_many(items_data)

# Save Query Parameters in Search [Audit]
search_query = {
    "author": 'crawler',
    "searched_link": news_url,
    "number_items": len(items_data),
    "host": client.HOST,
    'port': client.PORT,
    "searchedTime": datetime.datetime.now(tz=datetime.timezone.utc)
}

# Save query in log collection
searches = db_connection.get_collection('crawler_logs')
searched = searches.insert_one(search_query)