from llm_sdk import Small_LLM_Model
from constrained_decoder import GenState, mask_logits


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
            break
        if state == GenState.IN_PARAMETER_VALUE_STRING \
                and best_token_str == '"':
            break
        if state == GenState.IN_PARAMETER_VALUE_NUMBER\
                and best_token_str in (',', '}'):
            current_ids.pop()
            break
    return (current_ids, typed)





    