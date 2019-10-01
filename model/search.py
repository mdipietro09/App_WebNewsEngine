
import pandas as pd
import numpy as np

from model import nlp_utils



class search():
    
    def __init__(self, dtf_tweets, dtf_news):
        self.dtf_tweets = dtf_tweets if len(dtf_tweets) > 0 else 0
        self.dtf_news = dtf_news if len(dtf_news) > 0 else 0
        
    
    def data(self):
        if len(self.dtf_news)==0 and len(self.dtf_tweets)==0:
            return "No Data"
        else:
            ## tweets
            self.dtf_tweets = self.dtf_tweets.drop_duplicates("Tweet", keep='first')
            self.dtf_tweets = self.dtf_tweets[self.dtf_tweets["RTs"] >= self.dtf_tweets["RTs"].mean()]
            ### sentiment
            self.dtf_tweets = nlp_utils.add_sentiment(self.dtf_tweets, column="Tweet")
            self.dtf_tweets = self.dtf_tweets[(self.dtf_tweets["sentiment"] >= self.dtf_tweets["sentiment"].quantile(q=0.95)) |
                                          (self.dtf_tweets["sentiment"] <= self.dtf_tweets["sentiment"].quantile(q=0.05))]
            self.dtf_tweets = self.dtf_tweets.sort_values("sentiment", ascending=False)
            ### hashtags
            self.dtf_tweets["tags"] = self.dtf_tweets[["#","@","$"]].apply(lambda x: 
                           [ dic["text"] for dic in x[0] ] +
                           [ dic["name"] for dic in x[1] ] +
                           [ dic["text"] for dic in x[2] ],
                           axis=1)
            ### return data
            lst_tweets = self.dtf_tweets[["User","Location","Tweet","sentiment","tags"]].to_dict("records")
            
            ## news
            self.dtf_news = self.dtf_news.drop_duplicates("title", keep='first')
            ### sentiment
            self.dtf_news = nlp_utils.add_sentiment(self.dtf_news, column="title")
            self.dtf_news = self.dtf_news[(self.dtf_news["sentiment"] >= self.dtf_news["sentiment"].quantile(q=0.95)) |
                                          (self.dtf_news["sentiment"] <= self.dtf_news["sentiment"].quantile(q=0.05))]
            self.dtf_news = self.dtf_news.sort_values("sentiment", ascending=False)
            ### spacy
            self.dtf_news = nlp_utils.ner_spacy(self.dtf_news, column="title")
            ### return data
            lst_news = self.dtf_news[["source","title","content","url","sentiment","tags"]].to_dict("records")
            
            return lst_tweets, lst_news