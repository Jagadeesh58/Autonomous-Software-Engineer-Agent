"""
buggy.py - Demonstration file for agent bug-fixing capabilities.
"""


def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


if __name__ == "__main__":
    result = add(5, 3)
    print(f"5 + 3 = {result}")
    assert result == 8, "Addition test failed"
    print("Verification passed successfully.")
