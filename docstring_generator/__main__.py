from argparse import Namespace

from dotenv import load_dotenv

load_dotenv()
from .config import Config
from .docstring_generator import generate_docstrings
from .extensions import (
    failed_modules_queue,
    functions_source_code_queue,
    modules_path_queue,
    class_source_code_queue,
)
from .helpers import create_application_config, parse_arguments


def run():
    """Runs the application by parsing arguments, creating a configuration, and generating docstrings.

    Returns:
        function: The run function.
        docstring: The docstring for the run function.
        exceptions: Any exceptions that may be thrown during execution."""
    args: Namespace = parse_arguments()
    config: Config = create_application_config(args)
    generate_docstrings(
        config=config,
        module_path_queue=modules_path_queue,
        functions_source_queue=functions_source_code_queue,
        failed_modules_queue=failed_modules_queue,
        class_source_queue=class_source_code_queue,
    )


if __name__ == '__main__':
    run()
