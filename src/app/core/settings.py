from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    sqlalchemy_database_url: str
    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_db: str

    jwt_secret_key: str
    hash_algorithm: str
    access_token_expire_minutes: int
    # jwt_secret: str
    # jwt_algorithm: str = 'hs256'
    # jwt_expires_s: int = 3600


settings = Settings(
    _env_file='app/.env',
    _env_file_encoding='utf-8',
)
