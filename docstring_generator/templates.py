from langchain.prompts import PromptTemplate
from .config import Config


def get_function_prompt_template(function_code: str, config: Config) -> str:
    function_prompt_template: str = """
    You are an expert at generating docstrings for python functions. You will be provided with
    a python function without its docstrings. Your task is to generate the docstrinng for the
    function using the Numpy documentation style provided. Make sure to clearly describe what the
    function does, the inputs as well as the outputs. Also inlude example usage and the
    exceptions that the function may raise. Only return the function documentation without the
    function body.
    ####{function_code}####
    ####{documentation_style}####
    """
    prompt = PromptTemplate.from_template(template=function_prompt_template)
    prompt_formatted_str: str = prompt.format(
        function_code=function_code, documentation_style=config.documentation_style
    )
    return prompt_formatted_str
