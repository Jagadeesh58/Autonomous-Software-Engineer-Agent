"""
calculator.py - Basic calculator arithmetic operations.
"""


def add(x: float, y: float) -> float:
    return x + y


def subtract(x: float, y: float) -> float:
    return x - y


def multiply(x: float, y: float) -> float:
    return x * y


def divide(x: float, y: float):
    if y == 0:
        return 'Error: Division by zero is not allowed'
    return x / y


if __name__ == "__main__":
    print(f"2 + 3 = {add(2, 3)}")
    print(f"10 - 4 = {subtract(10, 4)}")
    print(f"6 * 7 = {multiply(6, 7)}")
    print(f"8 / 2 = {divide(8, 2)}")
