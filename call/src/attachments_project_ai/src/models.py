from attachments_project_ai.llm_sdk.llm_sdk import Small_LLM_Model


def sdk():

    sdk = Small_LLM_Model()

    test: str = "name\": \"fn_gre"

    names = ['fn_add_numbers', 'fn_greet', 'fn_reverse_string',
             'fn_get_square_root', 'fn_substitute_string_with_regex']
    f = []
    for n in names:
        if n.startswith('fn_gre'):
            f.append(n)
    print(f)
    ids = sdk.encode(test)
    ids = ids.tolist()
    ids = ids[0]
    logits = sdk.get_logits_from_input_ids(ids)
    logits = enumerate(logits)
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
