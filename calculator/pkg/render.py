# calculator/pkg/render.py

import json  # Used to serialise the output dictionary into a formatted JSON string


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    if isinstance(result, float) and result.is_integer():  # Check if the result is a whole number stored as a float (e.g. 5.0)
        result_to_dump = int(result)  # Convert to int so the JSON output shows 5 instead of 5.0
    else:
        result_to_dump = result  # Keep non-integer floats (e.g. 2.5) as-is

    output_data = {
        "expression": expression,  # The original expression string entered by the user
        "result": result_to_dump,  # The evaluated numeric result
    }
    return json.dumps(output_data, indent=indent)  # Serialise to a pretty-printed JSON string with the given indentation