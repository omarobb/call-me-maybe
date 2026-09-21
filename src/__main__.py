from .cli import loader
from .models import load_function_definitions, load_prompt_definitions, is_valid_string_continuation, build_token_loockup, load_function_name
from llm_sdk import Small_LLM_Model
from .generator import generate_one_call
if __name__ == "__main__":
    # print(is_valid_string_continuation("lo"))
    # print(is_valid_string_continuation("l\"o"))
    # print(is_valid_string_continuation("\""))
    # print(is_valid_string_continuation("lo"))
    # print(is_valid_string_continuation("lo\\"))
    # build_token_loockup(sdk)
    # print(loader())
    sdk = Small_LLM_Model()
    print(generate_one_call(sdk, "What is the sum of 22 and 3?",
                            load_function_definitions('data/input/functions_definition.json'),
                            load_function_name('data/input/functions_definition.json'),
                            build_token_loockup(sdk)))
