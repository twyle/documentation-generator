from argparse import ArgumentParser

from dotenv import load_dotenv

load_dotenv()
import os
from os import path

from .config import Config
from .docstring_generator import generate_docstrings
from .extensions import failed_modules_queue, modules_source_code_queue

parser: ArgumentParser = ArgumentParser()
parser.add_argument('--path', nargs='*', default=['.'], type=str)
parser.add_argument('--config-file', nargs='?', default='', type=str)
parser.add_argument('--OPENAI_API_KEY', nargs='?', default='', type=str)
parser.add_argument(
    '--overwrite-function-docstring', nargs='?', default=False, type=bool
)
parser.add_argument('--overwrite-class-docstring', nargs='?', default=False, type=bool)
parser.add_argument(
    '--overwrite-class-methods-docstring', nargs='?', default=False, type=bool
)
parser.add_argument('--directories-ignore', nargs='*', default=[], type=str)
parser.add_argument('--files-ignore', nargs='*', default=[], type=str)
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

config: Config = Config(
    path=set(paths),
    overwrite_function_docstring=args.overwrite_function_docstring,
    overwrite_class_docstring=args.overwrite_class_docstring,
    overwrite_class_methods_docstring=args.overwrite_class_methods_docstring,
)
config.directories_ignore.update(args.directories_ignore)
config.files_ignore.update(args.files_ignore)
generate_docstrings(
    config=config,
    module_source_queue=modules_source_code_queue,
    failed_modules_queue=failed_modules_queue,
)
