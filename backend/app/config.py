from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "My FastAPI project"
    oauth_token_secret: str = "my_dev_secret"
    debug_logs: bool = False
    SESSION_SECRET_KEY: str
    class Config:
        env_file = ".env"
        
settings = Settings()  # type: ignore