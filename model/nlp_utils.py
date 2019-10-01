
import pandas as pd
import numpy as np
from textblob import TextBlob
import collections
import spacy



def add_sentiment(dtf, column):
    dtf["sentiment"] = dtf[column].apply(lambda x: TextBlob(x).sentiment.polarity)
    return dtf
        
        
def lst_count(lst, top=None):
    dic_counter = collections.Counter()
    for x in lst:
        dic_counter[x] += 1
    dic_counter = collections.OrderedDict(sorted(dic_counter.items(), key=lambda x: x[1], reverse=True))
    lst_top = [ {key:value} for key,value in dic_counter.items() ]
    if top is not None:
        lst_top = lst_top[:top]
    return lst_top


def ner_spacy(dtf, column, tag_type=["ORG","PERSON"]):
    ner_model = spacy.load("instance/en_core_web_sm/en_core_web_sm-2.1.0")
    dtf["tags"] = dtf[column].apply(lambda x: [(word.text, word.label_) for word in ner_model(x).ents if word.label_ in tag_type] )
    dtf["tags"] = dtf["tags"].apply(lambda x: lst_count(x, top=None))
    return dtf