from .models import (load_function_definitions, load_prompt_definitions,
                     build_token_loockup, load_function_name)
from llm_sdk import Small_LLM_Model as LLM
from .generator import generate_one_call
from json import dump
import os


if __name__ == "__main__":
    sdk = LLM()
    OKBLUE = '\033[95m'
    GREEN = "\033[32m"
    RESET = "\033[0m"
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
    for i, pro in enumerate(prompt):
        print(f"{OKBLUE}Test {i+1}: {pro}{RESET}")
        print("------------------------------------"
              "------------------------------------")
        data = generate_one_call(sdk, pro.prompt,
                                 function_definitions,
                                 function_name,
                                 loockup).model_dump()
        final.append(data)
        print(f"{GREEN}{data}{RESET}")
        print("------------------------------------"
              "------------------------------------")
    with open('./data/output/function_calling_results.json', 'w') as f:
        dump(final, f, indent=4)
