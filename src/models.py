from llm_sdk.llm_sdk import Small_LLM_Model
from pydantic import BaseModel, ValidationError
from cli import loader
import sys
import json
# from typing import TextIO

names = []


class ParameterInfo(BaseModel):
    type: str


class FunctionEntry(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterInfo]
    returns: ParameterInfo


def sdk() -> None:

    sdk = Small_LLM_Model()

    test: str = "name\": \"fn_gre"

    f = []
    for n in names:
        if n.startswith('fn_gre'):
            f.append(n)
    print(f)
    ids = sdk.encode(test)
    ids = ids.tolist()
    ids = ids[0]
    logits = enumerate(sdk.get_logits_from_input_ids(ids))
    r = "et"
    best_value = None
    best_index = 0
    for idd, val in logits:
        s = sdk.decode([idd]) 
        if r.startswith(s):
            if best_value is None or val > best_value:
                best_value = val
                best_index = idd

    print(best_index, best_value, sdk.decode([best_index]))


def is_valid(s: str, typed: str, valid: list[str]) -> bool:
    return any(d for d in valid if d.startswith(typed + s))


def is_valid_integer_continuation(s: str, typed: str) -> bool:
    if s == '-' or s == '':
        if not typed:
            return True
    if typed:
        if typed[0] == '-':
            return (typed+s)[1:].isdigit()
    return (typed+s).isdigit()


def build_parameter_schema(fn_name: str,
                           fn_defintion: list[FunctionEntry])\
                           -> dict[str, ParameterInfo]:
    for fn in fn_defintion:
        if fn.name == fn_name:
            return fn.parameters
    raise ValueError("There is no function like that")


def load_function_definitions(path: str) -> list[str]:
    try:
        with open(path, 'r',  encoding='utf-8') as p:
            ls = json.load(p)
            for i in range(len(ls)):
                model_v = FunctionEntry.model_validate(ls[i])
                if isinstance(model_v, FunctionEntry):
                    names.append(ls[i]['name'])
            return names
    except (json.JSONDecodeError, FileNotFoundError, TypeError, ValidationError) as e:
        print(f"ERROR in JSON syntax: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print(is_valid("e", "fn_gre", names))
    print(is_valid("et", "fn_gre", names))
    print(is_valid("x", "fn_gre", names))
    print(is_valid("fn_greet", "", names))
    print(is_valid("fn_greeting", "", names))
    print("empty+digit (True):", is_valid_integer_continuation("5", ""))
    print("neg then digit (True):", is_valid_integer_continuation("5", "-"))
    print("dash first (True):", is_valid_integer_continuation("-", ""))
    print("double dash (False):", is_valid_integer_continuation("-", "-"))
    print("dash mid (False):", is_valid_integer_continuation("-", "5"))
    print("junk (False):", is_valid_integer_continuation("x", "5"))
    print("junk (False):", is_valid_integer_continuation("x", "65"))
    load_function_definitions("../input/functions_definition.json")