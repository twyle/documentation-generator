# documentation-generator
## Overeview
This is a python library for generating documentation for python projects. It is built to:
- Generate function docstrings
- Generate class docstrings include class method docstrings (still under development)
- Generate sphinx documentation (still under development)

The library uses ``openai's`` gpt model to generate the function docstrings. You pass it a file or folder path togther with an ``openai`` api key. It then parses the folder for python files, then for each file, it finds the functions and classes, generates their documentation and updates their docstrings.

## Requirements
- Python 3.10+
- Works on Linux, Windows, macOS, BSD

## Installation

```sh
pip install oryks-docstring-generator
```

## Usage

First, provide the ``openai``  api key:
```sh
export OPENAI_API_KEY=sk-xxxxxxxxxxx
```
Then run the application, providing the path to the python file to generate docs for or the folder containing the python files:
```sh
python -m docstring_generator --path test_function.py
```
