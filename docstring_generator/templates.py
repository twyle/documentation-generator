from langchain.prompts import PromptTemplate

from .config import Config


def get_function_prompt_template(function_code: str, config: Config) -> str:
    function_prompt_template: str = """
    Generate python docstring for the given python function using the provided documentation style:
    Function code: {function_code}
    Documentation style: {documentation_style}
    """
    prompt = PromptTemplate.from_template(template=function_prompt_template)
    prompt_formatted_str: str = prompt.format(
        function_code=function_code, documentation_style=config.documentation_style
    )
    return prompt_formatted_str


def get_class_prompt_template(class_code: str, config: Config) -> str:
    function_prompt_template: str = """
    Generate python docstring for the given python class using the provided documentation style:
    Class code: {class_code}
    Documentation style: {documentation_style}
    """
    prompt = PromptTemplate.from_template(template=function_prompt_template)
    prompt_formatted_str: str = prompt.format(
        class_code=class_code, documentation_style=config.documentation_style
    )
    return prompt_formatted_str
