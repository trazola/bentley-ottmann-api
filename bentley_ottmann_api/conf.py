from typing import Any, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    """
    Settings for `Geometry api` project.
    """

    db_user: str
    db_password: str
    db_name: str
    db_port: str
    db_host: str

    database_uri: Optional[PostgresDsn] = None

    @validator("database_uri", pre=True)
    def get_database_uri(cls, v: Optional[str], values: dict[str, Any]) -> Union[PostgresDsn, str]:
        """
        Method returns database uri.

        Args:
            v: value
            values: another value in class

        Returns:
            database uri
        """
        if v is None:
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("db_user"),
                password=values.get("db_password"),
                path=f"/{values.get('db_name')}",
                port=values.get("db_port"),
                host=values.get("db_host"),
            )
        return v

    class Config:
        env_file = ".env"


settings = Settings()
