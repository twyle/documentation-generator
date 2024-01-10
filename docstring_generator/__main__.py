from argparse import ArgumentParser

from dotenv import load_dotenv

load_dotenv()
import os
from os import path

from .config import Config
from .docstring_generator import generate_docstrings
from .extensions import failed_modules_queue, modules_queue, processed_modules_queue

parser: ArgumentParser = ArgumentParser()
parser.add_argument('--path', nargs='?', default='.', type=str)
parser.add_argument('--OPENAI_API_KEY', nargs='?', default='', type=str)
parser.add_argument('--overwrite-function-docstring', nargs='?', default=False, type=bool)
args = parser.parse_args()
source_code_dir: str = args.path

if not path.exists(source_code_dir):
    print(f"The target directory '{source_code_dir}' doesn't exist")
    raise SystemExit(1)

if args.OPENAI_API_KEY:
    os.environ['OPENAI_API_KEY'] = args.OPENAI_API_KEY

if not os.environ.get('OPENAI_API_KEY', None):
    print('You have not provided the open ai api key.')
    raise SystemExit(1)

config: Config = Config(
    path=source_code_dir,
    overwrite_function_docstring=args.overwrite_function_docstring
    )
generate_docstrings(
    config=config,
    modules_queue=modules_queue,
    processed_modules_queue=processed_modules_queue,
    failed_modules_queue=failed_modules_queue,
)
