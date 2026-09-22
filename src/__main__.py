from .models import (load_function_definitions, load_prompt_definitions,
                     build_token_loockup, load_function_name,
                     FunctionCallResult)
from llm_sdk import Small_LLM_Model
from .generator import generate_one_call
from json import dump
import os


if __name__ == "__main__":
    sdk = Small_LLM_Model()
    prompt = load_prompt_definitions('data/input/function_calling_tests.json')
    try:
        os.mkdir('./data/output')
    except FileExistsError:
        print("Directory already exists.")
    except PermissionError:
        print("Permission denied: Unable to create .")
    except Exception as e:
        print(f"An error occurred: {e}")
    final = []
    function_definitions = load_function_definitions(
                            'data/input/functions_definition.json')
    function_name = load_function_name(
                            'data/input/functions_definition.json')
    loockup = build_token_loockup(sdk)
    for pro in prompt:
        data = generate_one_call(sdk, pro.prompt,
                                 function_definitions,
                                 function_name,
                                 loockup).model_dump()
        final.append(data)
        print(data)
    with open('./data/output/function_calling_results.json', 'w') as f:
        dump(final, f, indent=4)
