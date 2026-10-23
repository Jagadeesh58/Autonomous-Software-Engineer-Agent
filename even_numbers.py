"""
even_numbers.py - Generate and print even numbers.
"""


def get_even_numbers(n: int) -> list:
    """Return a list of even numbers from 2 up to n (inclusive)."""
    return [i for i in range(2, n + 1, 2)]


if __name__ == "__main__":
    print(get_even_numbers(10))
