from pydantic_settings import BaseSettings



class Settings(BaseSettings):

    APP_NAME: str 

    APP_VERSION: float 

    DATABASE_URL: str 
    
    SECRET_KEY: str 

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15 

    ALGORITHM: str = "HS256"


    class Config:
        env_file = ".env"



def get_settings() -> Settings:

    return Settings() 