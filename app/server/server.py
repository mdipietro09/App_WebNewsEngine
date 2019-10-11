###############################################################################
#                                MAIN                                         #
###############################################################################

import flask
import pandas as pd

from model.eventregistry import eventregistry_engine
from model.newsapi import newsapi_engine
from model.twitter import twitter_engine
from model.discover import discover
from model.search import search

from instance.config.file_system import *



'''
'''
def create_app(twitter_keys, newsapi_keys, eventregistry_keys, name=None):
    ## app object
    name = name if name is not None else __name__
    app = flask.Flask(name, instance_relative_config=True, 
                      template_folder=dirpath+'app/client/templates',
                      static_folder=dirpath+'app/client/static')
        
    
    ## api
    @app.route('/ping', methods=["GET"])
    def ping():
        return 'pong'
    
    @app.route("/", methods=['GET', 'POST'])
    def index():
        try:
            newsapi = newsapi_engine(newsapi_keys)
            twitter = twitter_engine(twitter_keys)
            #eventregistry = eventregistry_engine(eventregistry_keys)
            
            if flask.request.method == 'POST':
                query = flask.request.form["query"]
                
                ### Search
                if query != "":
                    app.logger.info("--> Search")
                    query = query.split(",")
                    app.logger.info(query)
                    dtf_tweets = twitter.get_tweets(query)
                    app.logger.info('called Twitter')
                    dtf_news = newsapi.get_news(query)
                    app.logger.info('called Newsapi')
                    model = search(dtf_tweets, dtf_news)
                    tweets, news, topic_sentim, img = model.data()
                    app.logger.info(str(topic_sentim))
                    #dtf_events = eventregistry.get_events(query) 
                    return flask.render_template("search.html", tweets=tweets, news=news, 
                                                 topic_sentim=topic_sentim, img=img)
                
                ### Discover
                else:
                    app.logger.info("--> Discover")
                    dtf_tweets = twitter.discover_trends()
                    app.logger.info('called Twitter')
                    dtf_news = newsapi.discover_topnews()
                    app.logger.info('called Newsapi')
                    #dtf_events = eventregistry.discover_trendingconcepts()
                    model = discover(dtf_tweets, dtf_news)
                    tweets, news = model.data()
                    return flask.render_template("discover.html", tweets=tweets, news=news)
                
            else:
                return flask.render_template("index.html")
        except Exception as e:
            app.logger.error(e)
            flask.abort(500)
    
    
    ## errors
    @app.errorhandler(404)
    def page_not_found(e):
        return flask.render_template("errors.html", msg="Page doesn't exist"), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return flask.render_template('errors.html', msg="Something went terribly wrong"), 500
    
    
    return app