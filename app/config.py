from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    database_password:str
    database_name:str
    database_username:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int

    class Config:
        env_prefix = ''
        env_file = '../.env' 

    # class Config:
    #     env_file=".env"

settings=Settings()

print(settings.database_hostname)
