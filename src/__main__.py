from .cli import loader
from .models import load_function_definitions, load_prompt_definitions, is_valid_string_continuation, build_token_loockup
from llm_sdk import Small_LLM_Model
if __name__ == "__main__":
    print(is_valid_string_continuation("lo"))
    print(is_valid_string_continuation("l\"o"))
    print(is_valid_string_continuation("\""))
    print(is_valid_string_continuation("lo"))
    print(is_valid_string_continuation("lo\\"))
    sdk = Small_LLM_Model()
    build_token_loockup(sdk)
    print(loader())
    
