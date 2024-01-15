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
    make_docstring_node,
)


class FunctionDocStringWriter(NodeTransformer, BaseModel):
    module_code: str = Field(description='The source code for this module')
    config: Config = Field(description='The application configurations.')

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        '''
        def visit_FunctionDef(self, node: FunctionDef) -> Any:
            """
            Generates a docstring for a python function using the numpy-style documentation style.

            Parameters:
                node (FunctionDef): The python function to generate a docstring for.

            Returns:
                Any: The generated docstring for the function.

            Raises:
                None.

            Examples:
                >>> def add(x, y):
                ...     return x + y
                >>> visit_FunctionDef(add)
                'Adds two numbers together and returns the result.'

            """
            docstring: str = ast.get_docstring(node=node)
            if self.config.overwrite_function_docstring or not docstring:
                if docstring:
                    print("Deleting the existing docstring")
                    node.body.pop(0)
                function_code: str = ast.get_source_segment(
                    source=self.module_code, node=node, padded=True
                )
                function_docstring: str = generate_function_docstring(
                    function_code=function_code, config=self.config
                )
                new_docstring_node = make_docstring_node(function_docstring)
                node.body.insert(0, new_docstring_node)
            return node'''
        docstring: str = ast.get_docstring(node=node)
        if self.config.overwrite_function_docstring or not docstring:
            if docstring:
                print('Deleting the existing docstring')
                node.body.pop(0)
            function_code: str = ast.get_source_segment(
                source=self.module_code, node=node, padded=True
            )
            function_docstring: str = generate_function_docstring(
                function_code=function_code, config=self.config
            )
            new_docstring_node = make_docstring_node(function_docstring)
            node.body.insert(0, new_docstring_node)
        return node


class DocstringWriter(NodeTransformer, BaseModel):
    module_code: str = Field(description='The source code for this module')
    config: Config = Field(description='The application configurations.')

    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        '''
        def visit_FunctionDef(self, node: FunctionDef) -> Any:
            """
            Generates a docstring for a python function using the Numpy-style documentation format.

            Parameters:
                node (FunctionDef): The python function to generate a docstring for.

            Returns:
                Any: The generated docstring for the function.

            Raises:
                None.

            Examples:
                >>> def add(x, y):
                ...     return x + y
                >>> visit_FunctionDef(add)
                'Adds two numbers together and returns the result.'

            """
            docstring: str = ast.get_docstring(node=node)
            if self.config.overwrite_function_docstring or not docstring:
                function_code: str = ast.get_source_segment(
                    source=self.module_code, node=node, padded=True
                )
                function_and_docstring: str = generate_function_docstring(function_code)
                function_docstring: str = get_function_docstring(function_and_docstring)
                new_docstring_node = make_docstring_node(function_docstring)
                node.body.insert(0, new_docstring_node)
            return node'''
        docstring: str = ast.get_docstring(node=node)
        if self.config.overwrite_function_docstring or not docstring:
            function_code: str = ast.get_source_segment(
                source=self.module_code, node=node, padded=True
            )
            function_and_docstring: str = generate_function_docstring(function_code)
            function_docstring: str = get_function_docstring(function_and_docstring)
            new_docstring_node = make_docstring_node(function_docstring)
            node.body.insert(0, new_docstring_node)
        return node

    def visit_ClassDef(self, node: ClassDef) -> Any:
        '''
        def visit_ClassDef(self, node: ClassDef) -> Any:
            """
            Generates docstrings for a python class definition.

            Parameters:
                node (ClassDef): The class definition node to generate docstrings for.

            Returns:
                Any: The updated class definition node with docstrings added.

            Raises:
                None.

            Examples:
                >>> class MyClass:
                ...     def __init__(self, x):
                ...         self.x = x
                ...
                >>> visit_ClassDef(MyClass)
                MyClass:
                    """
                    Initializes a new instance of the MyClass class.

                    Parameters:
                        x (Any): The value to assign to the x attribute.

                    Returns:
                        None.

                    Raises:
                        None.

                    >>> class MyClass:
                    ...     def __init__(self, x):
                    ...         self.x = x
                    ...
                    >>> visit_ClassDef(MyClass)
                    MyClass:
                        """
                        Initializes a new instance of the MyClass class.

                        Parameters:
                            x (Any): The value to assign to the x attribute.

                        Returns:
                            None.

                        Raises:
                            None.
                        >>> class MyClass:
                        ...     def __init__(self, x):
                        ...         self.x = x
                        ...
        '''
        docstring: str = ast.get_docstring(node=node)
        if not docstring:
            class_code: str = ast.get_source_segment(
                source=self.module_code, node=node, padded=True
            )
            class_and_docstring: str = generate_class_docstring(class_code)
            class_docstring: str = get_class_docstring(class_and_docstring)
            new_docstring_node = make_docstring_node(class_docstring)
            node.body.insert(0, new_docstring_node)
            methods_docstrings: dict[str, str] = get_class_methods_docstrings(
                class_and_docstring
            )
            for class_node in node.body:
                if isinstance(class_node, FunctionDef):
                    function_doc: str = ast.get_docstring(node=class_node)
                    if not function_doc:
                        function_name: str = class_node.name
                        new_docstring_node = make_docstring_node(
                            methods_docstrings[function_name]
                        )
                        class_node.body.insert(0, new_docstring_node)
        return node
