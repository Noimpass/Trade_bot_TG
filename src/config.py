from dotenv import load_dotenv 
from pydantic_settings import BaseSettings

load_dotenv() # Initialize your env data.

class Settings(BaseSettings):
    '''
    Base settings for programm.

    Args:
        BaseSettings - pydantic object
    '''
    DB_USERNAME: str  # Username for database
    DB_NAME: str  # Name of database
    DB_PASSWORD: str  # Database password
    TDB_PORT: str  # Database port 5432 by default
    TDB_HOST: str  # Database host. localhost by default
    DB_HOST: str
    DB_PORT: str
    BOT_TOKEN: str  # Telegram bot token
    DATA_STORAGE: str  # Path to data_storage
    INSTRUCTIONS_FILE: str  # Path to instructions
    CARD_NUMBER: str
    PRICE: str

    TEST_SHOP_ID: str
    TEST_SHOP_ARTICLE_ID: str
    TEST_SHOP_TOKEN: str

Bot_on = True  # The bot is run by default.

settings = Settings()  # Initalizing this class object.