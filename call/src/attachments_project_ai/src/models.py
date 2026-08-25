from attachments_project_ai.llm_sdk.llm_sdk import Small_LLM_Model

names = ['fn_add_numbers', 'fn_greet', 'fn_reverse_string',
             'fn_get_square_root', 'fn_substitute_string_with_regex']
neg = False


def sdk():

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