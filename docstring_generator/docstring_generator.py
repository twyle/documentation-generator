from collections import deque

from .config import Config
from .file_processor import generate_file_docstrings, save_processed_files
from .helpers import get_all_modules


def generate_docstrings(
    config: Config,
    modules_queue: deque,
    processed_modules_queue: deque,
    failed_modules_queue: deque,
) -> None:
    """Generate docstrings for classes and methods."""
    get_all_modules(config=config, queue=modules_queue)
    generate_file_docstrings(
        modules_queue=modules_queue,
        processed_modules_queue=processed_modules_queue,
        failed_modules_queue=failed_modules_queue,
        config=config,
    )
    save_processed_files(processed_modules_queue=processed_modules_queue)
