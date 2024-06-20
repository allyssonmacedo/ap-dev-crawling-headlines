import requests
from bs4 import BeautifulSoup as bs


class Crawler():

    def __init__(self) -> None:
        pass

    def get_news_html(self, search_url: str = 'https://finance.yahoo.com/topic/latest-news/'):
        """This function verify the request status and returns the raw html researched when the request code is between (200,300)

        Args:
            search_url (string, optional): A string that contains a url link that leads to the website to scrape. Only the default link has been tested.
            Defaults to 'https://finance.yahoo.com/topic/latest-news/'.

        Raises:
            Exception: A error message

        Returns:
            The raw html scrapped webpage
        """
        rq = requests.get(search_url)   

        if rq.status_code in range(200, 300, 1):
            print(f'Scrapping de {search_url} finalizado com sucesso')
            
            return rq
        
        else:
            raise Exception("url inválido") 
    
    def get_news_soup(self, raw_html = None):
        """This function gets the raw html and return a parsed html that has been researched

        Args:
            raw_html (get_news_html(), optional): a raw html page. When the default is set (None) it will automatically performs the get_news_html(). Defaults to None.

        Returns:
            html: A parsed html
        """
        if raw_html == None:
            raw_html = self.get_news_html()

        soup = bs(raw_html.text, 'html.parser')
        return soup

    def get_news_items_html(self, soup=None, max_index=22):
        """This function gets the html for each item in the main researched page

        Args:
            soup (get_news_soup(), optional): a parsed html that will be filter to get the items html. Defaults to None.
            max_index (int, optional): the number of max items to return in the scrapping. Due the specifics of the page (currently), we can't perform more than 22 items each time. Defaults to 22.

        Returns:
            list: A list that contains the html of interest for each item in the main research
        """

        if soup == None: 
            soup = self.get_news_soup()

        list_items_raw = []

        soup_news = soup.select('.js-stream-content')

        for index_new in range(0, len(soup_news), 1):
            if index_new <= max_index - 1:
                soup_index = soup.select('.js-stream-content')[index_new]
                list_items_raw.append(soup_index)

        return list_items_raw
    
    def valid_info(self, field):
        """This function has the intent to verify the info that has been scrapped. 
           It only verifies if the field exists, if so, it will be collect, otherwise 'None' is returned

        Args:
            field (css element): the css element that will be catch in the scrapping

        Returns:
            It will return the element itself if exists, otherwise, it will return 'None' string
        """
        try:
            return field
        except:
            return 'None'
    
    def get_news_data(self, html_raw_list: None):
        """This functions gets the data for each item in the list of items collected. 

        Args:
            html_raw_list (get_news_items_html()): A list that was build before in the previously get_news_items_html() function. The code

        Returns:
            list: A list of dictionaries that contains the information for each item scrapped.
        """

        if html_raw_list == None:
            html_raw_list = self.get_news_items_html()

        search_data = [] 

        print(f'Coletando dados de {len(html_raw_list)} headlines')

        c = 1

        for item in html_raw_list:

            # coletando dados
            print(f'Coletando postagem de número {c}')

            # pegando a url
            url = item.h3.a['href']

            # pegando o headline
            headline = item.h3.text

            # coletando mais informações dentro de cada url
            news_page = requests.get(url)
        
            # fazendo o parse do html
            news_content = bs(news_page.text, 'html.parser')

            # pegando o autor da notícia
            author =  self.valid_info(news_content.select('.caas-attr-item-author')[0].text)

            # Datetime e a quantidade de minutos da notícia
            updated_time =  self.valid_info(news_content.select('.caas-attr-time-style'))

            datetime_news = self.valid_info(updated_time[0].time['datetime'])
            mins_read = self.valid_info(updated_time[0].select('.caas-attr-mins-read')[0].text.split()[0])

            # pegando outras características da notícia
            data_site = self.valid_info(news_content.select('.reactions-count')[0]['data-site'])
            data_source = self.valid_info(news_content.select('.reactions-count')[0]['data-source'])
            data_type = self.valid_info(news_content.select('.reactions-count')[0]['data-type'])
            count_comments = self.valid_info(news_content.select('.reactions-count')[0].text)
            
            news_data = {
                'url': url,
                'author': author,
                'headline': headline,
                'datetime_news': datetime_news,
                'mins_read': mins_read,
                'data_site': data_site,
                'data_source': data_source,
                'data_type': data_type,
                'count_comments': count_comments,
            }

            print(news_data)

            search_data.append(news_data)

            c += 1

        return search_data
    