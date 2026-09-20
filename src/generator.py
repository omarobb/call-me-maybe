from llm_sdk import Small_LLM_Model
from constrained_decoder import GenState, mask_logits
from models import build_token_loockup, build_priming_text, FunctionEntry, build_parameter_schema

def generate_field(sdk: Small_LLM_Model, current_ids: list[int],
                   typed: str, state: GenState,
                   valid_name: list[str],
                   token_lookup: dict[int, str]) -> tuple[list[int], str]:

    while True:
        logits = sdk.get_logits_from_input_ids(current_ids)
        masked = mask_logits(logits, typed, state, valid_name, token_lookup)
        h_token_id = masked.index(max(masked))
        best_token_str = token_lookup[h_token_id]
        current_ids.append(h_token_id)
        typed = typed+best_token_str

        if state == GenState.IN_FUNCTION_NAME and best_token_str == '"':
            # typed = typed[0:-1]
            break
        if state == GenState.IN_PARAMETER_VALUE_STRING \
                and best_token_str == '"':
            break
        if state == GenState.IN_PARAMETER_VALUE_NUMBER\
                and best_token_str in (',', '}'):
            current_ids.pop()
            typed = typed[0:-1]
            break
    return (current_ids, typed)


def generate_one_call(sdk: Small_LLM_Model, prompt_txt: str,
                      function_defs: list[FunctionEntry],
                      valid_names: list[str], token_lookup: dict[int, str]):

    priming_txt = build_priming_text(prompt_txt, function_defs)
    typed = '{\"name\": \"'
    current_ids = sdk.encode(priming_txt + typed).tolist()[0]

    current_ids, typed = generate_field(sdk, current_ids, typed,
                                        GenState.IN_FUNCTION_NAME,
                                        valid_names, token_lookup)
    
    function_name = typed.split('"')[3]
    schema = build_parameter_schema(function_name, function_defs)
    typed = typed + '\", \"parameters\": {'
    current_ids = sdk.encode(priming_txt + typed).tolist()[0]
    





    