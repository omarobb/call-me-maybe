import argparse
import json 
import sys

def loader():
    parser = argparse.ArgumentParser()
    argl = []
    parser.add_argument("--functions_definition",
                        default="data/input/functions_definition.json")
    parser.add_argument("--input",
                        default="data/input/function_calling_tests.json")
    parser.add_argument("--output",
                        default="data/output/function_calls.json")
    args = parser.parse_args()
    argl.append(args.functions_definition)
    argl.append(args.input)
    argl.append(args.output)

    try:
        with open(args.functions_definition, 'r') as f:
            fun = json.load(f)
        with open(args.input, 'r') as f:
            i = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, TypeError) as e:
        print(f"ERROR in JSON syntax: {e}")
        sys.exit(1)

    print(args.input)
    print(args.output)
    print(args.functions_definition)