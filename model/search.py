
import pandas as pd
import numpy as np
import re
from textblob import TextBlob
import collections
import spacy
import networkx
import matplotlib.pyplot as plt
import io
import base64



class search():
    
    def __init__(self, dtf_tweets, dtf_news):
        self.dtf_tweets = dtf_tweets if len(dtf_tweets) > 0 else 0
        self.dtf_news = dtf_news if len(dtf_news) > 0 else 0
    
    
    @staticmethod
    def clean_text_column(dtf, column):
        dtf["txt_clean"] = dtf[column].apply(lambda x: re.sub(r'[^\w\s]', '', str(x).lower().strip()) )   
        return dtf
    
    
    @staticmethod
    def add_sentiment(dtf, column):
        dtf["sentiment"] = dtf[column].apply(lambda x: TextBlob(x).sentiment.polarity)
        return dtf
    
    @staticmethod
    def lst_count(lst, top=None):
        dic_counter = collections.Counter()
        for x in lst:
            dic_counter[x] += 1
        dic_counter = collections.OrderedDict(sorted(dic_counter.items(), key=lambda x: x[1], reverse=True))
        lst_top = [ {key:value} for key,value in dic_counter.items() ]
        if top is not None:
            lst_top = lst_top[:top]
        return lst_top
    
    
    @staticmethod
    def ner_spacy(dtf, column, tag_type=["ORG","PERSON"]):
        ner_model = spacy.load("instance/en_core_web_sm/en_core_web_sm-2.1.0")
        dtf["tags"] = dtf[column].apply(lambda x: [word.text for word in ner_model(x).ents if word.label_ in tag_type] )
        return dtf
    
    
    def process_tweets(self, dtf, column="Tweet"):
        ## sentim
        dtf = self.clean_text_column(dtf, column=column)
        dtf = self.add_sentiment(dtf, column="txt_clean")
        sentim = dtf["sentiment"].sum()
        ## filter
        dtf = dtf.drop_duplicates(column, keep='first')
        dtf = dtf[dtf["RTs"] >= dtf["RTs"].mean()]
        dtf = dtf.sort_values("sentiment", ascending=False)
        ### hashtags
        dtf["tags"] = dtf[["#","@","$"]].apply(lambda x: [ dic["text"] for dic in x[0] ] +
                                                         [ dic["name"] for dic in x[1] ] +
                                                         [ dic["text"] for dic in x[2] ],
                                               axis=1)
        return dtf, sentim
     
            
    def process_news(self, dtf, column="description"):
        ## sentim
        dtf = self.clean_text_column(dtf, column=column)
        dtf = self.add_sentiment(dtf, column="txt_clean")
        sentim = dtf["sentiment"].sum()
        ## filter
        dtf = dtf.drop_duplicates(column, keep='first')
        dtf = dtf[(dtf["sentiment"] >= dtf["sentiment"].quantile(q=0.95)) | (dtf["sentiment"] <= dtf["sentiment"].quantile(q=0.05))]
        dtf = dtf.sort_values("sentiment", ascending=False)
        ### spacy
        dtf = self.ner_spacy(dtf, column=column)
        return dtf, sentim
    
    
    def extract_related_topics(self, lst, top=20, figsize=(15,8)):
        ## filter
        lst = list(filter(lambda x: x!=[], lst))
        ## flat
        lst = [x for lista in lst for x in lista]
        ## count    
        lst_dics = self.lst_count(lst, top=top)
        ## plot graph
        dtf_nodes = pd.DataFrame([ {'node':k,'attr':v} for dic in lst_dics for k,v in dic.items() ]).set_index('node')
        dtf_links = pd.DataFrame([ {'from':"", 'to':k} for dic in lst_dics for k in dic.keys()])
        G = networkx.from_pandas_edgelist(dtf_links, source="from", target="to", edge_attr=None)
        dtf_nodes = dtf_nodes.reindex( G.nodes() )
        plt.figure(figsize=figsize)
        networkx.draw(G, with_labels=True, node_size=dtf_nodes['attr'].values*1000, node_color=dtf_nodes['attr'].values, cmap=plt.cm.Dark2)
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='png')
        bytes_image.seek(0)
        bytes_image_url = base64.b64encode(bytes_image.getvalue()).decode()
        return 'data:image/png;base64,{}'.format(bytes_image_url)
        
    
    def data(self):
        ## tweets
        self.dtf_tweets, tweets_sentim = self.process_tweets(self.dtf_tweets, column="Tweet")
        lst_tweets = self.dtf_tweets[["User","Location","Tweet","sentiment","tags"]].to_dict("records")
        
        ## news
        self.dtf_news, news_sentim = self.process_news(self.dtf_news, column="description")
        lst_news = self.dtf_news[["source","title","description","url","sentiment","tags"]].to_dict("records")
        
        ## topic_sentim
        topic_sentim = np.tanh((tweets_sentim + news_sentim -5)/10)
        
        ## related topics
        lst = self.dtf_tweets["tags"].tolist() + self.dtf_news["tags"].tolist()
        plot_graph = self.extract_related_topics(lst)
        
        return lst_tweets, lst_news, topic_sentim, plot_graph