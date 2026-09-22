from .cli import loader
from .models import load_function_definitions, load_prompt_definitions, is_valid_string_continuation, build_token_loockup, load_function_name
from llm_sdk import Small_LLM_Model
from .generator import generate_one_call
from json import dump
import os
import ast
if __name__ == "__main__":
    sdk = Small_LLM_Model()
    prompt = load_prompt_definitions('data/input/function_calling_tests.json')
    try:
        os.mkdir('./data/output')
    except FileExistsError:
        os.remove('./dataoutput/function_calling_results.json')
        print("Directory already exists.")
    except PermissionError:
        print("Permission denied: Unable to create .")
    except Exception as e:
        print(f"An error occurred: {e}")
    final = []
    data = {}
    for pro in prompt:
        data = ast.literal_eval(generate_one_call(sdk, pro.prompt,
                                                  load_function_definitions('data/input/functions_definition.json'),
                                                  load_function_name('data/input/functions_definition.json'),
                                                  build_token_loockup(sdk)))
        final.append(data)
        print(data)
    with open('./data/output/function_calling_results.json', 'a') as f:
        dump(final, f, indent=4)
    
    # print(generate_one_call(sdk, "Replace all vowels in 'Programming is fun' with asterisks",
    #                         load_function_definitions('data/input/functions_definition.json'),
    #                         load_function_name('data/input/functions_definition.json'),
    #                         build_token_loockup(sdk)))