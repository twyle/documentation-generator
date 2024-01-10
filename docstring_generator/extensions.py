from collections import deque

from langchain_openai import OpenAI

modules_queue: deque = deque()
processed_modules_queue: deque = deque()
failed_modules_queue: deque = deque()

llm = OpenAI(temperature=0)
