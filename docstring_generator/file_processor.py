import ast
from queue import Empty, Queue

from .config import Config
from .docstring_writer import DocstringWriter
from .helpers import format_file, save_processed_file


def generate_module_docstrings(
    module_source_queue: Queue,
    config: Config,
) -> None:
    """Generate docstrings for this file."""
    while True:
        try:
            module_path, module_code = module_source_queue.get()
            moduel_tree = ast.parse(module_code)
            transformer = DocstringWriter(module_code=module_code, config=config)
            new_tree = transformer.visit(moduel_tree)
            ast.fix_missing_locations(new_tree)
            new_module_code = ast.unparse(new_tree)
            print(new_module_code)
        except Empty:
            continue
        else:
            save_processed_file(
                file_path=module_path, processed_module_code=new_module_code
            )
            format_file(module_path)
            module_source_queue.task_done()
