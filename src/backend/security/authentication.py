from src.backend.core.init_settings import global_settings


def authenticate_user(username: str, password: str) -> bool:
    return username == global_settings.USER_NAME and password == global_settings.PASSWORD
