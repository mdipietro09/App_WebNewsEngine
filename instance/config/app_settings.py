
name = "Web News Engine"

host = "0.0.0.0"

threaded = False

debug = False

## dev
#port = 5000

#from instance.config.api_keys import *

## prod
import os
port = int(os.environ.get("PORT", 5000))

import ast
twitter_keys = ast.literal_eval(os.environ["twitter_keys"])
newsapi_keys = ast.literal_eval(os.environ["newsapi_keys"])
eventregistry_keys = ast.literal_eval(os.environ["eventregistry_keys"])




