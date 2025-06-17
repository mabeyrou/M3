from dotenv import load_dotenv
from os import getenv

load_dotenv()

DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///:memory:')