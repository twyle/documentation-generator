import ast
import os
import subprocess
from argparse import ArgumentParser, Namespace
from ast import AsyncFunctionDef, ClassDef, Constant, Expr, FunctionDef
from collections import deque
from os import listdir, path
from queue import Queue
from typing import Iterator

from langchain.prompts import PromptTemplate

from .config import Config
from .extensions import llm
from .templates import get_function_prompt_template, get_class_prompt_template


def generate_function_docstring(function_code: str, config: Config) -> str:
    prompt_formatted_str: str = get_function_prompt_template(
        function_code=function_code, config=config
    )
    function_and_docstring = llm.invoke(prompt_formatted_str)
    return function_and_docstring


def generate_class_docstring(class_code: str, config: Config) -> str:
    prompt_formatted_str: str = get_class_prompt_template(
        class_code=class_code, config=config
    )
    class_and_docstring = llm.invoke(prompt_formatted_str)
    return class_and_docstring


def get_class_docstring(class_and_docstring: str) -> str:
    """Get the class docstring."""
    class_tree = ast.parse(class_and_docstring)
    for node in class_tree.body:
        if isinstance(node, ClassDef):
            cls_docstring: str = ast.get_docstring(node)
            return cls_docstring


def get_class_methods_docstrings(class_and_docstring: str) -> dict[str, str]:
    """Get a class methods docstrings."""
    class_methods: dict[str, str] = {}
    class_tree = ast.parse(class_and_docstring)
    for node in class_tree.body:
        if isinstance(node, ClassDef):
            for class_node in node.body:
                if isinstance(class_node, FunctionDef):
                    class_methods[class_node.name] = ast.get_docstring(class_node)
    return class_methods


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
    module_src: str = ''
    if module_path:
        module_src = get_module_source_code(module_path)
    module_source_queue.put((module_path, module_src))


def add_module_to_queue(module_path: str, module_path_queue: Queue):
    module_path_queue.put(module_path)


def get_node_source(node, module_src: str) -> str:
    return ast.get_source_segment(source=module_src, node=node)


def get_functions_source(module_path: str) -> list[str]:
    functions_src: list[str] = []
    module_src = get_module_source_code(module_path)
    module_tree = ast.parse(module_src)
    for node in module_tree.body:
        if isinstance(node, FunctionDef):
            function_src: str = get_node_source(node=node, module_src=module_src)
            functions_src.append((node.name, function_src))
    return functions_src


def get_class_source(module_path: str) -> None:
    class_src: list[str] = []
    module_src = get_module_source_code(module_path)
    module_tree = ast.parse(module_src)
    for node in module_tree.body:
        if isinstance(node, ClassDef):
            classsrc: str = get_node_source(node=node, module_src=module_src)
            class_src.append((node.name, classsrc))
    return class_src


class DirectoryIterator:
    def __init__(self, config: Config):
        self.config: Config = config
        self.queue: deque[str] = deque(self.config.path)

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
                        if (
                            entry_path not in self.config.files_ignore
                            and entry.split('.')[-1] == 'py'
                        ):
                            files.append(entry_path)
                    elif entry not in self.config.directories_ignore:
                        self.queue.append(entry_path)
            return files
        else:
            raise StopIteration()


def get_all_modules(config: Config, module_path_queue: Queue) -> None:
    """Iterate throug all the directories from the root directory."""
    for entry in config.path:
        if os.path.isfile(entry):
            add_module_to_queue(entry, module_path_queue)
        else:
            directory_iterator: DirectoryIterator = DirectoryIterator(config=config)
            for modules in directory_iterator:
                for module in modules:
                    add_module_to_queue(module, module_path_queue)


def save_processed_file(file_path: str, processed_module_code: str) -> None:
    """Save a processed file."""
    try:
        with open(file_path, 'w') as f:
            f.write(processed_module_code)
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)


def format_file(file_path: str) -> None:
    """Format the file using black."""
    if os.path.exists(file_path):
        subprocess.run(['black', file_path], capture_output=True)


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog='docstring-generator',
        description='Generate docstrings for your python projects',
        epilog='Thanks for using %(prog)s! :)',
    )
    parser.add_argument('--path', nargs='*', default=['.'], type=str)
    parser.add_argument('--config-file', nargs='?', default='', type=str)
    parser.add_argument('--OPENAI_API_KEY', nargs='?', default='', type=str)
    parser.add_argument(
        '--overwrite-function-docstring', nargs='?', default=False, type=bool
    )
    parser.add_argument(
        '--overwrite-class-docstring', nargs='?', default=False, type=bool
    )
    parser.add_argument(
        '--overwrite-class-methods-docstring', nargs='?', default=False, type=bool
    )
    parser.add_argument('--directories-ignore', nargs='*', default=[], type=str)
    parser.add_argument('--files-ignore', nargs='*', default=[], type=str)
    parser.add_argument(
        '--documentation-style',
        nargs='?',
        default='Numpy-Style',
        choices=['Numpy-Style', 'Google-Style', 'Sphinx-Style'],
        type=str,
    )
    args = parser.parse_args()
    paths: list[str] = args.path
    for entry in paths:
        if not path.exists(entry):
            print(f"The target directory '{entry}' doesn't exist")
            raise SystemExit(1)
    if args.OPENAI_API_KEY:
        os.environ['OPENAI_API_KEY'] = args.OPENAI_API_KEY
    if not os.environ.get('OPENAI_API_KEY', None):
        print('You have not provided the open ai api key.')
        raise SystemExit(1)
    return args


def create_application_config(args: Namespace) -> Config:
    config: Config = Config(
        path=set(args.path),
        overwrite_function_docstring=args.overwrite_function_docstring,
        overwrite_class_docstring=args.overwrite_class_docstring,
        overwrite_class_methods_docstring=args.overwrite_class_methods_docstring,
        documentation_style=args.documentation_style,
    )
    config.directories_ignore.update(args.directories_ignore)
    config.files_ignore.update(args.files_ignore)
    return config
