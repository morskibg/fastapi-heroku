import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = 'g!F$Aa#)'
    # SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    SERVER_NAME: str = 'https://softuni-react-backend.herokuapp.com/'
    # https://backend-react-powerapp.herokuapp.com/
    SERVER_HOST: AnyHttpUrl = 'http://localhost:8080'
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost", "http://localhost:4200", "http://localhost:3000",
                                              "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com", "http://10.10.10.71:3000", "https://softuni-react-powerapp.herokuapp.com", "https://softuni-react-backend.herokuapp.com",  "https://softuni-react-powerapp-morskibg.vercel.app", "https://softuni-react-powerapp.vercel.app/", "https://softuni-react-powerapp.vercel.app"
                                              ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = 'softuni-backend'
    # SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = "postgresql://ntxryrmkaudgpt:ecc84daa6ef96bf4041adfee079f1a0ca7317704b570efe0bcdcadf5e153e4bd@ec2-54-217-195-234.eu-west-1.compute.amazonaws.com:5432/detism4ur5phed"

    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None

    # @validator("EMAILS_FROM_NAME")
    # def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
    #     if not v:
    #         return values["PROJECT_NAME"]
    #     return v

    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    # EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )
    EQ_API_KEY: str = 'ab5e81-7adacb-92a6ae-2185c9'
    EMAIL_TEST_USER: EmailStr = "dimityrp@yahoo.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "dimityrp@yahoo.com"
    FIRST_SUPERUSER_PASSWORD: str = '12345'
    USERS_OPEN_REGISTRATION: bool = True
    EMAIL_GUEST_USER: EmailStr = "guestUser@demo.com"
    STP_CODES: list = ['EPRO_B01', 'EPRO_B02', 'EPRO_B03', 'EPRO_B04',           'EPRO_H01', 'EPRO_H02', 'EPRO_S01', 'EVN_BD000', 'EVN_G0', 'EVN_G1',
                       'EVN_G2', 'EVN_G3', 'EVN_G4', 'EVN_H0', 'EVN_H1', 'EVN_H2', 'CEZ_B1', 'CEZ_B2', 'CEZ_B3', 'CEZ_B4', 'CEZ_B5', 'CEZ_H1', 'CEZ_H2', 'CEZ_S1']

    class Config:
        case_sensitive = True


settings = Settings()
