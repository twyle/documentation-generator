from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    path: str = Field(description='The path to the source code directory')
    overwrite_function_docstring: Optional[bool] = Field(
        description='Whether or not to overwrite the existing function docstring',
        default=False,
    )
    directories_ignore: list[str] = Field(
        description='Directories to ignore',
        default=[
            'venv',
        ],
    )
