from dotenv import load_dotenv
from os import getenv
from os.path import join

load_dotenv()

ENVIRONMENT = getenv('ENVIRONMENT', 'development')
DATABASE_URL = getenv('DATABASE_URL', 'sqlite:///:memory:')
DEFAULT_MODEL_FILENAME = getenv('MODEL_FILENAME', 'new_ethically_strict_model.keras')
DEFAULT_MODEL_PATH = getenv('MODEL_PATH', join('.', 'models', DEFAULT_MODEL_FILENAME))
DEFAULT_PREPROCESSOR_FILENAME = getenv('PREPROCESSOR_FILENAME', 'new_ethically_strict_preprocessor.pkl')
DEFAULT_PREPROCESSOR_PATH = getenv('PREPROCESSOR_PATH', join('.', 'models', DEFAULT_PREPROCESSOR_FILENAME))