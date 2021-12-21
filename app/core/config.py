import secrets
from dotenv import load_dotenv
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "g!F$Aa#)"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    SERVER_NAME: str = "https://softuni-react-backend.herokuapp.com/"

    SERVER_HOST: AnyHttpUrl = "http://localhost:8080"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:4200",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://local.dockertoolbox.tiangolo.com",
        "http://10.10.10.71:3000",
        "https://softuni-react-powerapp.herokuapp.com",
        "https://softuni-react-backend.herokuapp.com",
        "https://softuni-react-powerapp-morskibg.vercel.app",
        "https://softuni-react-powerapp.vercel.app",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "softuni-backend"

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]

    EMAILS_ENABLED: bool = False

    EQ_API_KEY: Optional(str)

    EMAIL_TEST_USER: EmailStr = "dimityrp@yahoo.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "dimityrp@yahoo.com"
    FIRST_SUPERUSER_PASSWORD: str = "12345"
    USERS_OPEN_REGISTRATION: bool = True
    EMAIL_GUEST_USER: EmailStr = "guestUser@demo.com"
    STP_CODES: list = [
        "EPRO_B01",
        "EPRO_B02",
        "EPRO_B03",
        "EPRO_B04",
        "EPRO_H01",
        "EPRO_H02",
        "EPRO_S01",
        "EVN_BD000",
        "EVN_G0",
        "EVN_G1",
        "EVN_G2",
        "EVN_G3",
        "EVN_G4",
        "EVN_H0",
        "EVN_H1",
        "EVN_H2",
        "CEZ_B1",
        "CEZ_B2",
        "CEZ_B3",
        "CEZ_B4",
        "CEZ_B5",
        "CEZ_H1",
        "CEZ_H2",
        "CEZ_S1",
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
