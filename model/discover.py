
import pandas as pd
import numpy as np



class discover():
    
    def __init__(self, dtf_tweets, dtf_news):
        self.dtf_tweets = dtf_tweets if len(dtf_tweets) > 0 else 0
        self.dtf_news = dtf_news if len(dtf_news) > 0 else 0
        
    
    def data(self):
        ## tweets
        dic_tweets = {}
        for place in self.dtf_tweets.columns:
            dic_tweets.update({place:self.dtf_tweets[place].tolist()})
        #lst_tweets = [x for lista in self.dtf_tweets.values.tolist() for x in lista]
        
        ## news
        dic_news = {}
        for source in self.dtf_news["source"].unique():
            dic_news.update({source:self.dtf_news[self.dtf_news["source"] == source]["title"].tolist()})
        #lst_dics_news = self.dtf_news[["title", "source"]].to_dict("records")
        
        return dic_tweets, dic_news