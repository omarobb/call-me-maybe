import argparse
from .models import load_function_definitions, load_prompt_definitions


def loader():
    parser = argparse.ArgumentParser()
    fun_def = []
    fun_prompt = []
    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        default="data/output/function_calls.json")
    args = parser.parse_args()
    fun_def.append(load_function_definitions(args.functions_definition))
    fun_prompt.append(load_prompt_definitions(args.input))
#    print(fun_d)
    # print(args.inpu   t)
    # print(args.output)
    # print(args.functions_definition)
    return (fun_def, fun_prompt)
