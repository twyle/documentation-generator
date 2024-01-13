from typing import List, Optional

from pydantic import BaseModel, Field


class Config(BaseModel):
    path: set[str] = Field(description='The path to the source code directory')
    overwrite_function_docstring: Optional[bool] = Field(
        description='Whether or not to overwrite the existing function docstring',
        default=False,
    )
    overwrite_class_docstring: Optional[bool] = Field(
        description='Whether or not to overwrite the existing class docstring',
        default=False,
    )
    overwrite_class_methods_docstring: Optional[bool] = Field(
        description='Whether or not to overwrite the existing class methods docstring',
        default=False,
    )
    documentation_style: Optional[str] = Field(
        description='The format of documentation to use',
        default='Numpy-Style',
        enum=['Numpy-Style', 'Google-Style', 'Sphinx-Style'],
    )
    directories_ignore: set[str] = Field(
        description='Directories to ignore',
        default={'venv', '.venv', '__pycache__', '.git', 'build', 'dist', 'docs'},
    )
    files_ignore: set[str] = Field(
        description='Files to ignore',
        default_factory=set,
    )
