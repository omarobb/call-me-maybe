from llm_sdk import Small_LLM_Model
from .constrained_decoder import GenState, mask_logits
from typing import Any
from .models import (build_priming_text, FunctionEntry,
                     build_parameter_schema,
                     FunctionCallResult,
                     has_repeating_tail)
import time
import re


def generate_field(sdk: Small_LLM_Model, current_ids: list[int],
                   typed: str, state: GenState,
                   valid_name: list[str],
                   token_lookup: dict[int, str],
                   int_value: list[Any]) -> tuple[list[int], str]:
    field_typed = ""
    go = True
    while go:
        start = time.time()
        logits = sdk.get_logits_from_input_ids(current_ids)
        # print(f"step took {time.time()-start:.2f}s, seq len {len(current_ids)}, typed so far: {typed!r}")

        masked = mask_logits(logits, field_typed,
                             state, valid_name, token_lookup)
        h_token_id = masked.index(max(masked))
        best_token_str = token_lookup[h_token_id]
        current_ids.append(h_token_id)
        typed = typed+best_token_str
        if field_typed and field_typed.isdigit():
            if any(v for v in int_value if int(field_typed) == int(v) or float(field_typed) == int(v)):
                if len(int_value) > 1:
                    best_token_str = ','
                else:
                    best_token_str = '}'
        field_typed += best_token_str
        if state == GenState.IN_PARAMETER_VALUE_STRING:
            for block_size in [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 15, 17, 18, 19, 20]:
                if has_repeating_tail(field_typed, block_size):
                    typed = typed[:-block_size] + '"'
                    go = False
                    break
        if state == GenState.IN_FUNCTION_NAME and best_token_str == '"':
            typed = typed[0:-1]
            break
        if state == GenState.IN_PARAMETER_VALUE_STRING \
                and best_token_str == '"':
            break
        if state == GenState.IN_PARAMETER_VALUE_NUMBER\
                and best_token_str in (',', '}'):
            current_ids.pop()
            typed = typed[0:-1]
            field_typed = field_typed[0:-1]
            break
    return (current_ids, typed)


def generate_one_call(sdk: Small_LLM_Model, prompt_txt: str,
                      function_defs: list[FunctionEntry],
                      valid_names: list[str],
                      token_lookup: dict[int, str]) -> str:
    int_value = re.findall(r'\d+', prompt_txt)

    priming_txt = build_priming_text(prompt_txt, function_defs)
    typed = '{"name": "'
    current_ids = sdk.encode(priming_txt + typed).tolist()[0]
    current_ids, typed = generate_field(sdk, current_ids, typed,
                                        GenState.IN_FUNCTION_NAME,
                                        valid_names, token_lookup, int_value)

    function_name = typed.split('"')[3]
    schema = build_parameter_schema(function_name, function_defs)
    typed = typed + '", "parameters": {'
    current_ids = sdk.encode(priming_txt + typed).tolist()[0]
    parameters = {}
    for i, (key, value) in enumerate(schema.items()):
        typed = typed + '"' + key + '": '
        if value.type == 'string':
            typed += '"'
        current_ids = sdk.encode(priming_txt+typed).tolist()[0]
        state = GenState.IN_PARAMETER_VALUE_STRING \
            if value.type == 'string' else GenState.IN_PARAMETER_VALUE_NUMBER
        typed_b = typed
        current_ids, typed = generate_field(sdk, current_ids, typed,
                                            state, valid_names,
                                            token_lookup, int_value)
        r_value = typed[len(typed_b):]

        try:
            if value.type == 'string':
                parameters[key] = r_value.rstrip('"')
            else:
                parameters[key] = int(r_value)
        except ValueError:
            break

        if i < len(schema)-1:
            typed += ', '
            current_ids = sdk.encode(priming_txt + typed).tolist()[0]
    typed += '}}'
    typed = typed[1:]
    return '{' \
           f'"prompt": "{prompt_txt}", {typed}'
