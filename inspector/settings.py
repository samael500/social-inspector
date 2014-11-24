import os
import sys
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# add dir to path for use import
path = join(BASE_DIR, 'inspector')
if path not in sys.path:
    sys.path.insert(0, path)

# define dir's
TEMPLATE_DIR = join(BASE_DIR, 'inspector', 'templates')
DATA_DIR = join(BASE_DIR, 'inspector', 'data')

# Twitter authentication information
# must be redefined in settings local
TWITTER_OAUTH_INFO = dict(
    app_key='Consumer Key (API Key)',
    app_secret='Consumer Secret (API Secret)',
    oauth_token='Access Token',
    oauth_token_secret='Access Token Secret',
)

# is debug
DEBUG = False

try:
    from settings_local import *  # noqa
except ImportError:
    pass
