from enum import IntEnum, unique

from pydantic_settings import BaseSettings, SettingsConfigDict


@unique
class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL_ERROR = 4


def GetLogLevel(log_level: int) -> LogLevel:
    try:
        if int(log_level) == 0: return LogLevel.DEBUG
        elif int(log_level) == 1: return LogLevel.INFO
        elif int(log_level) == 2: return LogLevel.WARN
        elif int(log_level) == 3: return LogLevel.ERROR
        elif int(log_level) == 4: return LogLevel.CRITICAL_ERROR
        else: raise AttributeError
    except ValueError as VE: raise VE


class CONFIG(BaseSettings):
    # Telegram bot
    BOT_TOKEN: str
    TG_ID_OWNER: int
    TG_USERNAME_OWNER: str
    TG_FIRST_NAME_OWNER: str
    TG_LAST_NAME_OWNER: str | None = None
    NAME_ROLE_OWNER: str
    ID_ROLE_OWNER: int
    NAME_ROLE_DEFAULT: str
    ID_ROLE_DEFAULT: int
    REQUESTS_TIMEOUT: int

    # Backend
    BACKEND_CONTAINER_NAME: str
    BACKEND_PORT: int
    LOG_LEVEL: LogLevel
    LOG_FILE_NAME: str
    VERSION_MAJOR: str
    VERSION_MINOR: str
    VERSION_PATCH: str
    VERSION_TYPE: str
    RELEASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_CONTAINER_NAME: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: str
    NO_FOUND_HOMEWORK_MSG: str
    SECRET_KEY: str
    ALGORITHM: str
    SALT512: bytes

    # Other
    PROJECT_NAME: str
    SCHEDULE_CALL: list[dict[str, str]] = [
        {'start_time': '8.00', 'end_time': '8.45'},
        {'start_time': '8.55', 'end_time': '9.40'},
        {'start_time': '10.00', 'end_time': '10.45'},
        {'start_time': '11.05', 'end_time': '11.45'},
        {'start_time': '11.55', 'end_time': '12.35'},
        {'start_time': '12.45', 'end_time': '13.25'},
        {'start_time': '13.30', 'end_time': '14.10'},
        {'start_time': '14.15', 'end_time': '14.55'}
    ]

    model_config = SettingsConfigDict()
    

    def GetRelease(self) -> str:
        return str(f'Release {self.VERSION_MAJOR}.{self.VERSION_MINOR}.{self.VERSION_PATCH} [{self.VERSION_TYPE}]')


config = CONFIG()