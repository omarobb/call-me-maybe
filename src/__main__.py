from .cli import loader
from .models import sdk , load_function_definitions, load_prompt_definitions, is_valid_string_continuation

if __name__ == "__main__":
    print(is_valid_string_continuation('lo"'))
    print(is_valid_string_continuation('lo",'))
    print(is_valid_string_continuation('"'))
    print(is_valid_string_continuation('lo'))

    print(loader())
    
