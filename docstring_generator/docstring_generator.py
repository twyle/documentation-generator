from queue import Queue
from threading import Thread
from .config import Config
from .file_processor import generate_function_docstring, generate_module_docstrings
from .helpers import get_all_modules


def generate_docstrings(
    config: Config, module_source_queue: Queue, failed_modules_queue: Queue
) -> None:
    """Generate docstrings for classes and methods."""
    generate_source_code_thread: Thread = Thread(
        target=get_all_modules,
        name='generate_file_docstrings',
        args=(config, module_source_queue),
    )
    generate_source_code_thread.start()
    generate_functions_docstrings_thread: Thread = Thread(
        target=generate_function_docstring,
        name='generate_function_docstrings',
        args=(module_source_queue, config),
        daemon=True,
    )
    generate_functions_docstrings_thread.start()
    generate_source_code_thread.join()
    module_source_queue.join()
