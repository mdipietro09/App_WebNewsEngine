###############################################################################
#                            RUN MAIN                                         #
###############################################################################

from instance.config.app_settings import *
from instance.config.file_system import *
#from instance.config.api_keys import *
from app.server import server


import os
twitter_keys = os.environ["twitter_keys"]
newsapi_keys = os.environ["newsapi_keys"]
eventregistry_keys = os.environ["eventregistry_keys"]


app = server.create_app(name=name,
                        twitter_keys=twitter_keys, newsapi_keys=newsapi_keys, eventregistry_keys=eventregistry_keys)

app.run(host=host, port=port, threaded=threaded, debug=debug)