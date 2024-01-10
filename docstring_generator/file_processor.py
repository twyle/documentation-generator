import ast
from ast import ClassDef, FunctionDef
from collections import deque

from .config import Config
from .docstring_writer import DocstringWriter
from .helpers import format_file


def generate_file_docstrings(
    modules_queue: deque,
    processed_modules_queue: deque,
    failed_modules_queue: deque,
    config: Config,
) -> None:
    """Generate docstrings for this file."""
    while modules_queue:
        module_path, module_code = modules_queue.popleft()
        try:
            moduel_tree = ast.parse(module_code)
            transformer = DocstringWriter(module_code=module_code, config=config)
            new_tree = transformer.visit(moduel_tree)
            ast.fix_missing_locations(new_tree)
            new_module_code = ast.unparse(new_tree)
            print(new_module_code)
        except Exception as e:
            print(e)
            failed_modules_queue.append((module_path, module_code))
        else:
            processed_modules_queue.append((module_path, new_module_code))


def save_processed_files(processed_modules_queue: deque) -> None:
    """save the processed files."""
    while processed_modules_queue:
        module_path, module_code = processed_modules_queue.popleft()
        with open(module_path, 'w') as f:
            f.write(module_code)
        format_file(module_path)
