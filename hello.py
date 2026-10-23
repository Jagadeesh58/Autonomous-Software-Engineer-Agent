"""
hello.py - Basic greeting module.
"""


def say_hello(name: str = "World") -> str:
    """Return a greeting message."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(say_hello())
