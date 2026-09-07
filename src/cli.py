import argparse
from .models import load_function_definitions


def loader():
    parser = argparse.ArgumentParser()
    fun_d = []
    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        default="data/output/function_calls.json")
    args = parser.parse_args()
    fun_d.append(load_function_definitions(args.functions_definition))
    fun_d.append(load_function_definitions(args.input))
    fun_d.append(load_function_definitions(args.output))
#    print(fun_d)
    # print(args.input)
    # print(args.output)
    # print(args.functions_definition)
