from queue import Queue
from threading import Thread

from .config import Config
from .file_processor import (
    generate_function_docstrings,
    queue_unprocessed_functions_methods,
    generate_class_docstrings,
)
from .helpers import get_all_modules


def generate_docstrings(
    config: Config,
    module_path_queue: Queue,
    functions_source_queue: Queue,
    class_source_queue: Queue,
    failed_modules_queue: Queue,
) -> None:
    """Generate docstrings for classes and methods."""
    queue_modules: Thread = Thread(
        target=get_all_modules,
        name='get_all_modules',
        args=(config, module_path_queue),
    )
    queue_modules.start()

    for _ in range(1):
        get_functions_source_thread: Thread = Thread(
            target=queue_unprocessed_functions_methods,
            args=(functions_source_queue, class_source_queue, module_path_queue),
            daemon=True,
        )
        get_functions_source_thread.start()

    for _ in range(1):
        generate_functions_docstring_thread: Thread = Thread(
            target=generate_function_docstrings,
            args=(functions_source_queue, config),
            daemon=True,
        )
        generate_functions_docstring_thread.start()

    for _ in range(1):
        generate_class_docstring_thread: Thread = Thread(
            target=generate_class_docstrings,
            args=(class_source_queue, config),
            daemon=True,
        )
        generate_class_docstring_thread.start()

    queue_modules.join()
    module_path_queue.join()
    functions_source_queue.join()
    class_source_queue.join()
