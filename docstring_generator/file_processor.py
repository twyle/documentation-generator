import ast
from queue import Empty, Queue

from .config import Config
from .docstring_writer import ClassDocStringWriter, FunctionDocStringWriter
from .helpers import (
    format_file,
    get_class_source,
    get_functions_source,
    get_module_source_code,
    save_processed_file,
)


def queue_unprocessed_functions_methods(
    functions_source_queue: Queue, classes_source_queue: Queue, module_path_queue: Queue
) -> None:
    while True:
        try:
            module_path: str = module_path_queue.get()
            functions: list[str] = get_functions_source(module_path)
            for function_name, function_code in functions:
                functions_source_queue.put((module_path, function_name, function_code))
            classes: list[str] = get_class_source(module_path)
            for class_name, class_code in classes:
                classes_source_queue.put((module_path, class_name, class_code))
        except Empty:
            continue
        else:
            module_path_queue.task_done()


def generate_function_docstrings(functions_source_queue: Queue, config: Config) -> None:
    """Generate docstrings for this file."""
    while True:
        try:
            module_path, function_name, function_code = functions_source_queue.get()
            module_tree = ast.parse(get_module_source_code(module_path))
            transformer = FunctionDocStringWriter(
                module_path=module_path,
                function_name=function_name,
                function_code=function_code,
                config=config,
            )
            new_tree = transformer.visit(module_tree)
            ast.fix_missing_locations(new_tree)
            new_module_code = ast.unparse(new_tree)
        except Empty:
            continue
        except Exception as e:
            print(e)
            functions_source_queue.task_done()
            continue
        else:
            save_processed_file(
                file_path=module_path, processed_module_code=new_module_code
            )
            format_file(module_path)
            functions_source_queue.task_done()

def generate_class_docstrings(class_source_queue: Queue, config: Config) -> None:
    """Generate docstrings for this file."""
    while True:
        try:
            module_path, class_name, class_code = class_source_queue.get()
            module_tree = ast.parse(get_module_source_code(module_path))
            transformer = ClassDocStringWriter(
                module_path=module_path,
                class_name=class_name,
                class_code=class_code,
                config=config,
            )
            new_tree = transformer.visit(module_tree)
            ast.fix_missing_locations(new_tree)
            new_module_code = ast.unparse(new_tree)
        except Empty:
            continue
        except Exception as e:
            print(e)
            class_source_queue.task_done()
            continue
        else:
            save_processed_file(
                file_path=module_path, processed_module_code=new_module_code
            )
            format_file(module_path)
            class_source_queue.task_done()
