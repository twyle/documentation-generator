from argparse import Namespace

from dotenv import load_dotenv

load_dotenv()

from .config import Config
from .docstring_generator import generate_docstrings
from .extensions import failed_modules_queue, modules_source_code_queue
from .helpers import create_application_config, parse_arguments


def run():
    args: Namespace = parse_arguments()
    config: Config = create_application_config(args)
    generate_docstrings(
        config=config,
        module_source_queue=modules_source_code_queue,
        failed_modules_queue=failed_modules_queue,
    )


if __name__ == '__main__':
    run()
