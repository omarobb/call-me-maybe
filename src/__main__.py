from .cli import loader
from .models import sdk , load_function_definitions

if __name__ == "__main__":
    load_function_definitions("data/input/functions_definition.json")
