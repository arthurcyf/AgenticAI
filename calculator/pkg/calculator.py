# calculator/pkg/calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,  # Addition
            "-": lambda a, b: a - b,  # Subtraction
            "*": lambda a, b: a * b,  # Multiplication
            "/": lambda a, b: a / b,  # Division
        }  # Maps each operator symbol to its arithmetic function; used when applying an operator during evaluation
        self.precedence = {
            "+": 2,  # Lower precedence — evaluated after * and /
            "-": 2,  # Lower precedence — evaluated after * and /
            "*": 3,  # Higher precedence — evaluated before + and -
            "/": 3,  # Higher precedence — evaluated before + and -
        }  # Controls operator ordering in the shunting-yard algorithm so BODMAS/PEMDAS is respected

    def evaluate(self, expression):
        if not expression or expression.isspace():  # Reject blank or whitespace-only expressions
            return None  # Signal to the caller that there is nothing to evaluate
        tokens = expression.strip().split()  # Remove surrounding whitespace and split into individual tokens (numbers and operators)
        return self._evaluate_infix(tokens)  # Delegate to the infix evaluator and return the numeric result

    def _evaluate_infix(self, tokens):
        values = []   # Stack that holds numeric operands waiting to be consumed by an operator
        operators = []  # Stack that holds operators waiting to be applied once their right-hand operand is known

        for token in tokens:  # Process tokens left-to-right using the shunting-yard algorithm
            if token in self.operators:  # Current token is an operator
                while (
                    operators  # There is an operator already waiting on the stack
                    and operators[-1] in self.operators  # The top of the stack is also an operator (not a bracket)
                    and self.precedence[operators[-1]] >= self.precedence[token]  # The waiting operator has equal or higher precedence
                ):
                    self._apply_operator(operators, values)  # Apply the higher-precedence operator before pushing the current one
                operators.append(token)  # Push the current operator onto the stack
            else:
                try:
                    values.append(float(token))  # Parse the token as a number and push it onto the value stack
                except ValueError:
                    raise ValueError(f"invalid token: {token}")  # Token is neither a known operator nor a number

        while operators:  # Drain any remaining operators after all tokens are processed
            self._apply_operator(operators, values)  # Apply each remaining operator to the top two values

        if len(values) != 1:  # A well-formed expression must reduce to exactly one value
            raise ValueError("invalid expression")  # More than one value left means the expression was malformed

        return values[0]  # Return the single remaining value as the final result

    def _apply_operator(self, operators, values):
        if not operators:  # Guard: nothing to apply if the operator stack is empty
            return

        operator = operators.pop()  # Pop the most recently pushed operator
        if len(values) < 2:  # An operator needs exactly two operands
            raise ValueError(f"not enough operands for operator {operator}")  # Expression is invalid — missing a number

        b = values.pop()  # Pop the right-hand operand first (last pushed)
        a = values.pop()  # Pop the left-hand operand second
        values.append(self.operators[operator](a, b))  # Apply the operator to (a, b) and push the result back