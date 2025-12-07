from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str

    MONGO_URI: str
    MONGO_DB_NAME: str = "simple_chatbot_local"

    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: str = "19530"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
settings = Settings()