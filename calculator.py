import math
import os
import sys
from openai import OpenAI

class AdvancedCalculator:
    def __init__(self):
        self.history = []

    def evaluate_expression(self, expression: str):
        """
        Calculates standard mathematical expressions safely.
        """
        try:
            # Custom formatting for python syntax
            clean_expr = expression.replace('^', '**').replace('π', str(math.pi)).replace('e', str(math.e))
            
            # Safe namespace for math operations
            safe_dict = {
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "log": math.log10,
                "ln": math.log,
                "sqrt": math.sqrt,
                "factorial": math.factorial,
                "abs": abs,
                "pow": pow
            }
            
            result = eval(clean_expr, {"__builtins__": None}, safe_dict)
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            return f"Error: {str(e)}"

    def solve_with_ai(self, prompt: str):
        """
        Uses GPT to solve high-level word problems or step-by-step math problems.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "❌ OPENAI_API_KEY environment variable missing."

        try:
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert mathematical problem solver. Provide direct, accurate, step-by-step mathematical solutions."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"❌ AI Error: {str(e)}"


def run_tests():
    print("=======================================")
    print("🧮 Running High-Level Calculator Tests")
    print("=======================================")

    calc = AdvancedCalculator()

    # Test 1: Scientific math checks
    expr1 = "sin(90) + cos(0)"
    res1 = calc.evaluate_expression(expr1)
    print(f"Test 1 [{expr1}]: {res1}")
    assert res1 == 2.0, "Test 1 Failed!"

    # Test 2: Advanced functions (log & square root)
    expr2 = "sqrt(16) + log(100)"
    res2 = calc.evaluate_expression(expr2)
    print(f"Test 2 [{expr2}]: {res2}")
    assert res2 == 6.0, "Test 2 Failed!"

    # Test 3: AI Math Solver Test
    print("\n🤖 Testing AI Problem Solver...")
    ai_problem = "Solve for x: 3x + 15 = 45"
    ai_res = calc.solve_with_ai(ai_problem)
    print(f"AI Solution for '{ai_problem}':\n{ai_res}")

    print("\n✅ All Tests Passed Successfully!")

if __name__ == "__main__":
    run_tests()
