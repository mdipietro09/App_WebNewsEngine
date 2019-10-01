
import pandas as pd
import numpy as np
import tweepy



class twitter_engine():
    
    def __init__(self, twitter_keys):
        self.CONSUMER_KEY = twitter_keys["CONSUMER_KEY"]
        self.SECRET_KEY = twitter_keys["SECRET_KEY"]
        self.ACCESS_TOKEN = twitter_keys["ACCESS_TOKEN"]
        self.SECRET_ACCESS_TOKEN = twitter_keys["SECRET_ACCESS_TOKEN"]
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.SECRET_KEY)
        auth.set_access_token(self.ACCESS_TOKEN, self.SECRET_ACCESS_TOKEN)
        self.api = tweepy.API(auth)
        
    
    def get_tweets(self, filtri_lst, max_items=50):
        ## api request Cursor
        dic_tweets = {}
        for filtro in filtri_lst:
            cursor_obj= tweepy.Cursor(self.api.search, q=filtro, include_entities=True, exclude_replies=True, count=100, result_type="recent", lang="en").items(max_items)
            lst_tweets= []
            for tweet in enumerate(cursor_obj):
                lst_tweets.append(tweet[1])
                dic_tweets[filtro] = lst_tweets
        ## put it in dtf
        dtf_tweets = pd.DataFrame()
        for filtro, lst_tweets in dic_tweets.items():
            dtf = pd.DataFrame( data=[tweet.text for tweet in lst_tweets], columns=['Tweet'] )
            dtf['keyword'] = filtro
            dtf['ID'] = np.array([tweet.id for tweet in lst_tweets])
            dtf['Date'] = np.array([tweet.created_at for tweet in lst_tweets])
            dtf['User'] = [tweet.user.name for tweet in lst_tweets]
            dtf["Location"] = [tweet.user.location for tweet in lst_tweets]
            dtf["#"] = [tweet.entities.get("hashtags") for tweet in lst_tweets]
            dtf["@"] = [tweet.entities.get("user_mentions") for tweet in lst_tweets]
            dtf["$"] = [tweet.entities.get("symbols") for tweet in lst_tweets]
            dtf['Source'] = np.array([tweet.source for tweet in lst_tweets])
            dtf['Likes'] = np.array([tweet.favorite_count for tweet in lst_tweets])
            dtf['RTs'] = np.array([tweet.retweet_count for tweet in lst_tweets])
            dtf_tweets = dtf_tweets.append(dtf, ignore_index=True)
        return dtf_tweets


    def discover_trends(self, top=20, dic_places={"World":1, 
                                                  "USA":23424977, "Canada":23424775, 
                                                  "UK":23424975, "France":23424819, "Germany":23424829, "Italy":23424853, "Spain":23424950,
                                                  "Russia":23424936, "Japan":23424856, "Emirates":23424738}):
        dic_trends = {}
        for where, id_place in dic_places.items():
            res = self.api.trends_place(id_place)
            dic = res[0] 
            lst = dic['trends']
            lst_trends = [trend['name'] for trend in lst]
            dic_trends[where] = lst_trends[0:top]
        dtf_trends = pd.DataFrame.from_dict(dic_trends)
        return dtf_trends.head(top)