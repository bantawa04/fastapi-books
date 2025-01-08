from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGO: str
    REDIS_HOST:str ="localhost"
    REDIS_PORT:int =6379
    REDIS_PASSWORD:str="secret_redis"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# add this line
Config = Settings()
