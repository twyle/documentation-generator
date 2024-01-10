import ast
import os
import subprocess
from ast import AsyncFunctionDef, Constant, Expr, FunctionDef
from collections import deque

from langchain.prompts import PromptTemplate

from .config import Config
from .extensions import llm


def generate_function_docstring(function_code: str) -> str:
    function_prompt_template: str = """
    Write a NumPy-style docstring for the following function: {function}.
    Make sure to return the function and its docstring as well as the exceptions that maybe thrown.
    """
    prompt = PromptTemplate.from_template(template=function_prompt_template)
    prompt_formatted_str: str = prompt.format(function=function_code)
    function_and_docstring = llm.invoke(prompt_formatted_str)
    return function_and_docstring


def make_docstring_node(docstr: str):
    constant_str: Constant = Constant(docstr)
    return Expr(value=constant_str)


def get_function_docstring(function_and_docstring: str) -> str:
    """Get the function docstring."""
    function_tree = ast.parse(function_and_docstring)
    for node in function_tree.body:
        if isinstance(node, (FunctionDef, AsyncFunctionDef)):
            function_docstring: str = ast.get_docstring(node)
    return function_docstring


def get_module_source_code(module_path: str) -> str:
    """Get the source code for a given module."""
    with open(module_path, 'r') as f:
        return f.read()


def add_module_to_queue(module_path: str, queue: deque):
    module_src: str = get_module_source_code(module_path)
    queue.append((module_path, module_src))


def get_all_modules(config: Config, queue: deque) -> None:
    """Iterate throug all the directories from the root directory."""
    if os.path.isfile(config.path):
        add_module_to_queue(config.path, queue)
    else:
        for root_directory, directories, modules in os.walk(config.path, topdown=False):
            for module_name in modules:
                if module_name.split('.')[-1] == 'py':
                    add_module_to_queue(
                        os.path.join(root_directory, module_name), queue
                    )


def format_file(file_path: str) -> None:
    """Format the file using black."""
    subprocess.run(['black', file_path])
