###############################################################################
#                            RUN MAIN                                         #
###############################################################################

from instance.config.app_settings import *
from instance.config.file_system import *
from app.server import server



app = server.create_app(name=name,
                        twitter_keys=twitter_keys, newsapi_keys=newsapi_keys, 
                        eventregistry_keys=eventregistry_keys)

app.run(host=host, port=port, threaded=threaded, debug=debug)