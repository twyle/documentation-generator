from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    path: str = Field(description='The path to the source code directory')
    overwrite_function_docstring: Optional[bool] = Field(
        description='Whether or not to overwrite the existing function docstring',
        default=False,
    )
    documentation_style: Optional[str] = Field(
        description='The format of documentation to use', default='Numpy-Style'
    )
    directories_ignore: set[str] = Field(
        description='Directories to ignore',
        default={
            'venv', '__pycache__', '.git', 'build', 'dist', 'docs'
        },
    )
