# Statement for enabling the development environment
DEBUG = True

# Application name
TITLE = 'Monitor'
# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__)) + '/'

# Define Persistant Storage
DB_SERVER = "mongodb://localhost:27017"
DB_NAME = "monitor"

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 4

# Enable protection agains *Cross-site Request Forgery (CSRF)
WTF_CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = ""

# url base
SERVER_URL = 'http://localhost:5000'

#email
MAIL_SERVER=""
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
CRM_BCC = ""
REPLY_TO = ""
