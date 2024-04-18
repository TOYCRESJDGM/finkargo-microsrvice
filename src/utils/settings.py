import os
from dotenv import load_dotenv

load_dotenv(".env")
ENVIRONMENT = os.environ.get('ENVIRONMENT')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
APP_PORT= os.environ.get('APP_PORT')
JWT_KEY = os.environ.get('JWT_KEY')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')
DB_USER_NAME = os.environ.get('DB_USER_NAME')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
ACCOUNT_SID=os.environ.get('ACCOUNT_SID')
AUTH_TOKEN=os.environ.get('AUTH_TOKEN')
LIMIT_TIME=os.environ.get('LIMIT_TIME')
URL_MESSAGES=os.environ.get('URL_MESSAGES')
URL_COUNTRIES=os.environ.get('URL_COUNTRIES')