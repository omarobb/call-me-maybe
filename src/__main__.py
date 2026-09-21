from .cli import loader
from .models import load_function_definitions, load_prompt_definitions, is_valid_string_continuation, build_token_loockup, load_function_name
from llm_sdk import Small_LLM_Model
from .generator import generate_one_call

if __name__ == "__main__":
    sdk = Small_LLM_Model()
    prompt = load_prompt_definitions('data/input/function_calling_tests.json')
    for pro in prompt:
        print(generate_one_call(sdk, pro.prompt,
                                load_function_definitions('data/input/functions_definition.json'),
                                load_function_name('data/input/functions_definition.json'),
                                build_token_loockup(sdk)))
    
