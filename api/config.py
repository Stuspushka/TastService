import os

def get_env_var(name: str, required: bool = True, default=None):
    val = os.getenv(name, default)
    if required and (val is None or val == ""):
        raise RuntimeError(f"Environment variable '{name}' is not set or empty")
    return val

def get_env_int(name: str, required: bool = True, default=None) -> int:
    val = get_env_var(name, required, default)
    try:
        return int(val)
    except (TypeError, ValueError):
        raise RuntimeError(f"Environment variable '{name}' must be an integer")

class Settings:
    DATABASE_URL: str = get_env_var("DATABASE_URL")
    RABBITMQ_URL: str = get_env_var("RABBITMQ_URL")
    RABBITMQ_QUEUE_NAME: str = get_env_var("RABBITMQ_QUEUE_NAME")
    WORKER_TIMEOUT: int = get_env_int("WORKER_TIMEOUT", default=600000)
    MAX_RETRIES: int = get_env_int("MAX_RETRIES", default=3)
    API_PORT: int = get_env_int("PORT", default=3000)
    NODE_ENV: str = get_env_var("NODE_ENV", required=False, default="development")

settings = Settings()
