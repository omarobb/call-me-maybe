from enum import Enum


class GenState(Enum):
    IN_FUNCTION_NAME = "in_function_name"
    IN_PARAMETER_VALUE_STRING = "in_parameter_value_string"
    IN_PARAMETER_VALUE_NUMBER = "in_parameter_value_number"
    
