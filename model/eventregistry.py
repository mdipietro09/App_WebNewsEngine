
import pandas as pd
import eventregistry as evr



class eventregistry_engine():
    
    def __init__(self, eventregistry_keys):
        self.KEY = eventregistry_keys["KEY"]
        self.api = evr.EventRegistry(apiKey=self.KEY)


    @staticmethod
    def fun_category_titles(categories):
            return [category['uri'].replace('dmoz/', '') for category in categories]


    @staticmethod
    def fun_relevance(event, concept_uri):
            relevance = [concept['score'] for concept in event['concepts'] if concept['uri'] == concept_uri]
            if relevance:
                return relevance[0]
            else:
                return 0


    def get_events(self, filtri_lst, language="eng", relevance_threshold=20):
        ## api request getConcept e getCategory
        concept_uris = [self.api.getConceptUri(filtro) for filtro in filtri_lst]
        ## api request QueryEvents
        q = evr.QueryEvents( conceptUri=evr.QueryItems.AND(concept_uris), lang=language )
        q.setRequestedResult( evr.RequestEventsInfo(sortBy="rel", count=10) )  #sortBy options: date, rel(relevance to the query), size(number of articles), socialScore(popularity on social media)
        lst_events = self.api.execQuery(q)['events']['results']
        ## Filter out irrelevant events
        lst_relevant_events = []
        for event in lst_events:
            if event["uri"][0:3] == "eng":
                dic_event = {}
                dic_event = {'uri':event['uri'], 'date':event['eventDate'], 'title':event['title']['eng'], 'categories':self.fun_category_titles(event['categories'])}
                for concept_uri in concept_uris:
                    if max( [self.fun_relevance(event, concept_uri) ]) > relevance_threshold:
                        lst_relevant_events.append(dic_event)
                    else:
                        next
            else:
                next
        ## api request RequestEventArticles
        dtf_events = pd.DataFrame(columns=['keyword', 'event_date', 'event_uri', 'event_title', 'event_categories', 'article_date', 'article_time', 'article_source', 'article_title', 'article_body'])
        for event in lst_relevant_events:
            q = evr.QueryEvent(event['uri'])
            q.setRequestedResult( evr.RequestEventArticles(count=50, sortBy='date', lang=language) )
            articles = self.api.execQuery(q)[event['uri']]['articles']['results']
            dtf_event_article = pd.DataFrame([{'keyword': filtri_lst,
                                            'event_date': event['date'],
                                            'event_uri': event['uri'],
                                            'event_title': event['title'],
                                            'event_categories': event['categories'],
                                            'article_date': article['date'],
                                            'article_time': article['time'],
                                            'article_source': article['source']['title'],
                                            'article_title': article['title'],
                                            'article_body': article['body']} for article in articles])
            dtf_events = dtf_events.append(dtf_event_article, sort=False)                
        return dtf_events

        
    def discover_trendingconcepts(self, top=20):
        ## api request GetTrendingConcepts
        q = evr.GetTrendingConcepts(source="news", count=top)
        
        q = evr.GetTrendingConcepts(source="pr", count=top, conceptType=['org'], returnInfo=evr.ReturnInfo(conceptInfo=evr.ConceptInfoFlags(trendingHistory=True)))
        ret = api.execQuery(q)        
        ## create dic_concepts
        dic_concepts = {concept['uri']: concept['trendingHistory']['news'] for concept in ret}
        print(dic_concepts.keys())
        ## api request QueryEvents
        lst_events = []
        for concept_uri in dic_concepts:
            print(concept_uri)
            q = evr.QueryEvents( conceptUri=concept_uri )
            q.setRequestedResult( evr.RequestEventsInfo(sortBy="rel", count=1) )
            event = self.api.execQuery(q)['events']['results']
            if event:
                event = event[0]
                event.update({'search_term': concept_uri.replace('http://en.wikipedia.org/wiki/', '')})
                event.update({'trendingHistory': dic_concepts[concept_uri]})
                lst_events.append(event)
        return dtf_concepts
        
    