import ast
import os
import subprocess
from ast import AsyncFunctionDef, Constant, Expr, FunctionDef
from queue import Queue
from typing import Optional, Iterator
from os import path, listdir
import os
from collections import deque

from langchain.prompts import PromptTemplate

from .config import Config
from .extensions import llm

function_doc: str = '''
def add(a: int, b: int) -> int:
    """Returns the sum of two integers.

    Parameters:
    a (int): First integer.
    b (int): Second integer.

    Returns:
    int: Sum of a and b.

    Raises:
    TypeError: If either a or b is not an integer."""
    return a + b
'''


# def generate_function_docstring(function_code: str) -> str:
#     return function_doc


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


def add_module_code_to_queue(module_path: str, module_source_queue: Queue):
    print(module_path)
    module_src: str = ''
    if module_path:
        module_src = get_module_source_code(module_path)
    module_source_queue.put((module_path, module_src))


def add_module_to_queue(module_path: str, module_source_queue: Queue):
    add_module_code_to_queue(
        module_path=module_path, module_source_queue=module_source_queue
    )


class DirectoryIterator:
    def __init__(
        self,
        config: Config,
    ):
        self.config: Config = config
        self.queue: deque[str] = deque([self.config.path])

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> list[str]:
        files: list[str] = list()
        if self.queue:
            for _ in range(len(self.queue)):
                root_dir: str = self.queue.popleft()
                if root_dir.split('/')[-1] in self.config.directories_ignore:
                    continue
                entries: list[str] = listdir(root_dir)
                for entry in entries:
                    entry_path: str = path.join(root_dir, entry)
                    if path.isfile(entry_path):
                        if entry.split('.')[-1] == 'py':
                            files.append(entry_path)
                    else:
                        if entry not in self.config.directories_ignore:
                            self.queue.append(entry_path)
            return files
        else:
            raise StopIteration()


def get_all_modules(config: Config, module_source_queue: Queue) -> None:
    """Iterate throug all the directories from the root directory."""
    if os.path.isfile(config.path):
        add_module_to_queue(config.path, module_source_queue)
    else:
        directory_iterator: DirectoryIterator = DirectoryIterator(config=config)
        for modules in directory_iterator:
            for module in modules:
                add_module_to_queue(
                    module, module_source_queue
                )


def save_processed_file(file_path: str, processed_module_code: str) -> None:
    """Save a processed file."""
    with open(file_path, 'w') as f:
        f.write(processed_module_code)


def format_file(file_path: str) -> None:
    """Format the file using black."""
    subprocess.run(['black', file_path])
