
import pandas as pd
from newsapi import NewsApiClient
import math



class newsapi_engine():
    
    def __init__(self, newsapi_keys):
        self.KEY = newsapi_keys["KEY"]
        self.api = NewsApiClient(api_key=self.KEY)


    def get_news(self, filtri_lst, language="en", top=20):
        ## api request get_everything
        dic_news = {}
        for filtro in filtri_lst:
            dic_news[filtro] = {}
            dic_news[filtro][1] = self.api.get_everything(q=filtro, sort_by='relevancy', language=language, page_size=top, page=1)
            pages = min((math.ceil(dic_news[filtro][1]['totalResults']/100)), 5)
            for page in range(2, pages+1):
                dic_news[filtro][page] = self.api.get_everything(q=filtro, sort_by='relevancy', language=language, page_size=top, page=page)
        ## transform dic into lst
        lst_news = []
        search_nr = 1
        for k_1, v_1 in dic_news.items():
            for k_2, v_2 in v_1.items():
                for article in v_2['articles']:
                    lst_news.append((search_nr, v_2['totalResults'], k_1, article['author'], article['content'], article['description'], article['publishedAt'], article['source']['name'], article['title'], article['url'], article['urlToImage']))
            search_nr += 1
        ## transform lst into dtf
        dtf_news = pd.DataFrame(lst_news, columns=['nrSearch', 'totalResults', 'keyword', 'author', 'content', 'description', 'publishedAt', 'source', 'title', 'url', 'urlToImage'])
        return dtf_news
    
    
    def discover_topnews(self, language="en"):
        ## api request get_top_headlines
        dic_headlines = self.api.get_top_headlines(language=language)
        ## transform json into dtf
        dtf_headlines = pd.DataFrame(columns=["source", "author", "title", "description", "content", "url", "publishedAt"])
        for json in dic_headlines["articles"]:
            dic_article = {}
            dic_article["source"] = [json["source"]["name"]]
            dic_article["author"] = [json["author"]]
            dic_article["title"] = [json["title"]]
            dic_article["description"] = [json["description"]]
            dic_article["content"] = [json["content"]]
            dic_article["url"] = [json["url"]]
            dic_article["publishedAt"] = [json["publishedAt"]]
            dtf_article = pd.DataFrame.from_dict(dic_article)
            dtf_headlines = dtf_headlines.append(dtf_article, ignore_index=True)
        return dtf_headlines
    