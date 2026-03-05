# calculator/main.py

import sys  # Provides access to command-line arguments via sys.argv
from pkg.calculator import Calculator  # The Calculator class that parses and evaluates infix expressions
from pkg.render import format_json_output  # Formats the result as a pretty-printed JSON string


def main():
    calculator = Calculator()  # Create a Calculator instance (loads operator definitions and precedence rules)
    if len(sys.argv) <= 1:  # No expression was passed — print usage instructions and exit
        print("Calculator App")  # Print the app name
        print('Usage: python main.py "<expression>"')  # Show how to run the script correctly
        print('Example: python main.py "3 + 5"')  # Provide a concrete example
        return  # Exit early — nothing to calculate

    expression = " ".join(sys.argv[1:])  # Join all CLI arguments to support expressions that may be split by the shell
    try:
        result = calculator.evaluate(expression)  # Evaluate the mathematical expression and return a float
        if result is not None:  # None means the expression was blank or whitespace-only
            to_print = format_json_output(expression, result)  # Serialise the expression and result as JSON
            print(to_print)  # Print the JSON to stdout (captured by run_python_file if called via the agent)
        else:
            print("Error: Expression is empty or contains only whitespace.")  # Inform the caller the expression was blank
    except Exception as e:
        print(f"Error: {e}")  # Print any evaluation errors (e.g. invalid tokens, insufficient operands)


if __name__ == "__main__":
    main()  # Entry point: run main() when this script is executed directly