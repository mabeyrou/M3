from dotenv import load_dotenv
from os import getenv

load_dotenv()

ENVIRONMENT = getenv('ENVIRONMENT', 'development')
DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///:memory:')