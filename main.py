from scr.crawler import Crawler

# Get the news html
crawler = Crawler()

news_html = crawler.get_news_html()

# Get the soup from the news
news_soup = crawler.get_news_soup(raw_html = news_html)

# Get the items news from the search
news_items = crawler.get_news_items_html(soup=news_soup, max_index=15)

# Get a list of data from each item
items_data = crawler.get_news_data(html_raw_list = news_items)
                      
print(items_data)

# print(crawler.test(10))




# jobs_url = JobScrapping().getJobsURL(search, max_jobs=10)

# soup_jobs = JobScrapping().getJobSoup(jobs_url)

# jobs_posts = []
# for job in soup_jobs:
#     post = JobScrapping().getJobPost(job)
#     jobs_posts.append(post)


# ### Save in Mongo DB
# client = connectmongo.connectServer()

# db_connection = client['jobs-in']

# collection = db_connection.get_collection('posts')

# data = collection.insert_many(jobs_posts)

# ### Save Query Parameters in Search
# search_query = {
#     "author": 'crawler',
#     "searchedLink": search,
#     "searchedJobs": jobs_url,
#     "searchedParameters": JobScrapping().getSearchParameters(search),
#     "searchedTime": datetime.datetime.now(tz=datetime.timezone.utc),
# }

# searches = db_connection.get_collection('searches')
# searched = searches.insert_one(search_query)