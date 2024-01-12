from queue import Queue

from langchain_openai import OpenAI

modules_path_queue: Queue = Queue()
modules_source_code_queue: Queue = Queue()
processed_modules_queue: Queue = Queue()
failed_modules_queue: Queue = Queue()

llm = OpenAI(temperature=0)
