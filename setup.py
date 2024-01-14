from setuptools import find_packages, setup
from pip._vendor import tomli
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
with open('pyproject.toml', 'r') as f:
    VERSION = tomli.load(f)['tool']['commitizen']['version']
DESCRIPTION = 'A python library for generating documentation for python projects.'
key_words = ['dosctrings', 'documentation']
install_requires = [
    'langchain',
    'langchain-openai',
    'black',
    'pydantic',
    'pydantic-settings',
]
setup(
    name='oryks-docstring-generator',
    packages=find_packages(include=['docstring_generator']),
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    url='https://youtube-wrapper.readthedocs.io/en/latest/index.html',
    author='Lyle Okoth',
    author_email='lyceokoth@gmail.com',
    license='MIT',
    install_requires=install_requires,
    keywords=key_words,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Operating System :: OS Independent',
    ],
)
