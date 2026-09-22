from llm_sdk import Small_LLM_Model
from pydantic import BaseModel, ValidationError, TypeAdapter
# from cli import loader
import sys
import json
# from typing import Any
# from typing import TextIO


class ParameterInfo(BaseModel):
    type: str


class Prompt(BaseModel):
    prompt: str


class FunctionEntry(BaseModel):
    name: str
    description: str
    parameters: dict[str, ParameterInfo]
    returns: ParameterInfo


class FunctionCallResult(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, (int | str | float)]


def is_complete_name(typed: str, valid: list[str]) -> bool:
    return typed in valid


def is_valid(s: str, typed: str, valid: list[str]) -> bool:
    return any(d for d in valid if d.startswith(typed + s))


def is_name_token_allowed(candidate_token: str,
                          typed: str, valid: list[str]) -> bool:
    if candidate_token == '"':
        return is_complete_name(typed, valid)
    else:
        return is_valid(candidate_token, typed, valid)


def is_valid_string_continuation(s: str) -> bool:
    if '"' in s:
        if not s[-1] == '"':
            return False
        if s.count('"') > 1:
            return False
    if s.endswith('\\'):
        return False
    return True


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
    for fun in fn_defintion:
        if fun.name == fn_name:
            return fun.parameters
    raise ValueError("There is no function like that")


def load_function_definitions(path: str) -> list[FunctionEntry]:
    try:
        with open(path, 'r', encoding='utf-8') as p:
            ls = json.load(p)
            validation = TypeAdapter(list[FunctionEntry])
            return validation.validate_python(ls)
    except (json.JSONDecodeError, FileNotFoundError,
            TypeError, ValidationError) as e:
        print(f"ERROR in function_definitions: {e}")
        sys.exit(1)


def load_function_name(path: str) -> list[str]:
    try:
        with open(path, 'r', encoding='utf-8') as p:
            names = []
            ls = json.load(p)
            for fn in ls:
                names.append(fn['name'])
            return names
    except (json.JSONDecodeError, FileNotFoundError,
            TypeError, ValidationError) as e:
        print(f"ERROR in function_definitions: {e}")
        sys.exit(1)


def load_prompt_definitions(path: str) -> list[Prompt]:
    try:
        with open(path, 'r', encoding='utf-8') as p:
            ls = json.load(p)
            validation = TypeAdapter(list[Prompt])
            return validation.validate_python(ls)
    except (json.JSONDecodeError, FileNotFoundError,
            TypeError, ValidationError) as e:
        print(f"ERROR in prompt_definitions: {e}")
        sys.exit(1)


def build_token_loockup(sdk: Small_LLM_Model) -> dict[int, str]:
    ids = sdk.encode('a')
    ids = ids.tolist()[0]
    log = sdk.get_logits_from_input_ids(ids)
    vocab_size = len(log)
    lookup = {}
    for token_id in range(vocab_size):
        lookup[token_id] = sdk.decode([token_id])
    return lookup


def build_priming_text(prompt_text: str,
                       function_defs: list[FunctionEntry]) -> str:
    instruction = (
        "/no_think",
        "Select exactly one available function that can fulfill the request.",
        "Compare the meaning of the request with each function description.",
        "Different wording or synonyms still count as a match.",
        "Extract every required parameter from the request.",
        "Copy string values exactly and do not invent additional content.",
        "Return only the function-call JSON object without explanations or",
        " additional text."
    )

    function_json = TypeAdapter(list[FunctionEntry]).dump_json(function_defs)

    return f"{instruction} \n\n Available functions: \n"\
           f"{function_json}\n\n User request: \n{prompt_text}\n\n"


def has_repeating_tail(field_typed: str, block_size: int) -> bool:
    if len(field_typed) < block_size * 2:
        return False

    last_block = field_typed[-block_size:]
    previous_block = field_typed[-block_size*2: -block_size]
    return last_block == previous_block
