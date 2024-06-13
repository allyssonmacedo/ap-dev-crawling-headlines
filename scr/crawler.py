import requests
from bs4 import BeautifulSoup as bs


class Crawler():

    def __init__(self) -> None:
        pass

    def get_news_html(self, search_url: str = 'https://finance.yahoo.com/topic/latest-news/'):
        rq = requests.get(search_url)   

        if rq.status_code in range(200, 300, 1):
            print(f'Scrapping de {search_url} finalizado com sucesso')
            
            return rq
        
        else:
            raise Exception
        
    def get_news_soup(self, raw_html=get_news_html()):
        soup = bs(raw_html.text, 'html.parser')
        return soup

    def get_news_items_html(self, soup=get_news_soup(), max_index=22):
        list_items_raw = []

        soup_news = soup.select('.js-stream-content')

        for index_new in range(0, len(soup_news), 1):
            if index_new <= max_index:
                soup_index = soup.select('.js-stream-content')[index_new]
                list_items_raw.append(soup_index)

        return list_items_raw
    
    def get_news_data(html_raw_list: list = get_news_items_html()):

        search_data = [] 

        for item in html_raw_list:

            # pegando a url
            url = item.h3.a['href']

            # pegando o headline
            headline = item.h3.text

            # coletando mais informações dentro de cada url
            news_page = requests.get(url)
        
            # fazendo o parse do html
            news_content = bs(news_page.text, 'html.parser')

            # pegando o autor da notícia
            author = news_content.select('.caas-attr-item-author')[0].text

            # Datetime e a quantidade de minutos da notícia
            updated_time = news_content.select('.caas-attr-time-style')

            datetime_news = updated_time[0].time['datetime']
            mins_read = updated_time[0].select('.caas-attr-mins-read')[0].text.split()[0]

            # pegando outras características da notícia
            data_site = news_content.select('.reactions-count')[0]['data-site']
            data_source = news_content.select('.reactions-count')[0]['data-source']
            data_type = news_content.select('.reactions-count')[0]['data-type']
            count_comments = news_content.select('.reactions-count')[0].text
            
            news_data = {
                'url': url if len(url) > 0 else 'None',
                'author': author if len(author) > 0  else 'None',
                'headline': headline if len(headline) > 0 else 'None',
                'datetime_news': datetime_news if len(datetime_news) > 0 else 'None',
                'mins_read': mins_read if len(mins_read) > 0 else 'None',
                'data_site': data_site if len(data_site) > 0 else 'None',
                'data_source': data_source if len(data_source) > 0 else 'None',
                'data_type': data_type if len(data_type) > 0 else 'None',
                'count_comments': count_comments if len(count_comments) > 0 else 'None'
            }
        
            search_data.append(news_data)

        return search_data
