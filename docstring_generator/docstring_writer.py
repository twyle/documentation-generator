import ast
from _ast import ClassDef, FunctionDef
from ast import NodeTransformer
from typing import Any

from pydantic import BaseModel, Field

from .config import Config
from .helpers import (
    generate_class_docstring,
    generate_function_docstring,
    get_class_docstring,
    get_class_methods_docstrings,
    get_function_docstring,
    get_module_source_code,
    make_docstring_node,
)


class FunctionDocStringWriter(NodeTransformer, BaseModel):
    module_path: str = Field(description='The path to this module')
    function_name: str = Field(
        description='The name of the function to generate docstrings'
    )
    function_code: str = Field(description='The source code for this function')
    config: Config = Field(description='The application configurations.')

    @property
    def module_code(self) -> str:
        return get_module_source_code(self.module_path)

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        docstring: str = ast.get_docstring(node=node)
        if node.name == self.function_name and (
            self.config.overwrite_function_docstring or not docstring
        ):
            function_code: str = ast.get_source_segment(
                source=self.module_code, node=node, padded=True
            )
            function_and_docstring: str = generate_function_docstring(
                function_code=function_code, config=self.config
            )
            try:
                function_docstring: str = get_function_docstring(function_and_docstring)
            except Exception:
                new_docstring_node = make_docstring_node(function_and_docstring)
            else:
                new_docstring_node = make_docstring_node(function_docstring)
            node.body.insert(0, new_docstring_node)
        return node


class ClassDocStringWriter(NodeTransformer, BaseModel):
    module_path: str = Field(description='The path to this module')
    class_name: str = Field(description='The name of the class to generate docstrings')
    class_code: str = Field(description='The source code for this class')
    config: Config = Field(description='The application configurations.')

    @property
    def module_code(self) -> str:
        return get_module_source_code(self.module_path)

    def visit_ClassDef(self, node: ClassDef) -> Any:
        docstring: str = ast.get_docstring(node=node)
        if node.name == self.class_name and (
            self.config.overwrite_class_docstring or not docstring
        ):
            class_code: str = ast.get_source_segment(
                source=self.module_code, node=node, padded=True
            )
            class_and_docstring: str = generate_class_docstring(
                class_code=class_code, config=self.config
            )
            try:
                class_docstring: str = get_class_docstring(class_and_docstring)
            except Exception:
                class_docstring = class_and_docstring
                new_docstring_node = make_docstring_node(class_and_docstring)
                class_docstring = class_and_docstring
            else:
                new_docstring_node = make_docstring_node(class_docstring)
            node.body.insert(0, new_docstring_node)
            methods_docstrings: dict[str, str] = get_class_methods_docstrings(
                class_and_docstring
            )
            for class_node in node.body:
                if isinstance(class_node, FunctionDef):
                    function_doc: str = ast.get_docstring(node=class_node)
                    if (
                        not function_doc
                        or self.config.overwrite_class_methods_docstring
                    ):
                        function_name: str = class_node.name
                        new_docstring_node = make_docstring_node(
                            methods_docstrings[function_name]
                        )
                        class_node.body.insert(0, new_docstring_node)
        return node


class DocstringWriter(NodeTransformer, BaseModel):
    module_code: str = Field(description='The source code for this module')
    config: Config = Field(description='The application configurations.')

    def visit_classDef(self, node: FunctionDef) -> Any:
        docstring: str = ast.get_docstring(node=node)
        if self.config.overwrite_function_docstring or not docstring:
            function_code: str = ast.get_source_segment(
                source=self.module_code, node=node, padded=True
            )
            function_and_docstring: str = generate_function_docstring(
                function_code, self.config
            )
            function_docstring: str = get_function_docstring(function_and_docstring)
            new_docstring_node = make_docstring_node(function_docstring)
            node.body.insert(0, new_docstring_node)

        return node

    def visit_ClassDef(self, node: ClassDef) -> Any:
        docstring: str = ast.get_docstring(node=node)
        if not docstring or self.config.overwrite_class_docstring:
            class_code: str = ast.get_source_segment(
                source=self.module_code, node=node, padded=True
            )
            class_and_docstring: str = generate_class_docstring(class_code, self.config)
            class_docstring: str = get_class_docstring(class_and_docstring)
            new_docstring_node = make_docstring_node(class_docstring)
            node.body.insert(0, new_docstring_node)
            methods_docstrings: dict[str, str] = get_class_methods_docstrings(
                class_and_docstring
            )
            for class_node in node.body:
                if isinstance(class_node, FunctionDef):
                    function_doc: str = ast.get_docstring(node=class_node)
                    if (
                        not function_doc
                        or self.config.overwrite_class_methods_docstring
                    ):
                        function_name: str = class_node.name
                        new_docstring_node = make_docstring_node(
                            methods_docstrings[function_name]
                        )
                        class_node.body.insert(0, new_docstring_node)
        return node
