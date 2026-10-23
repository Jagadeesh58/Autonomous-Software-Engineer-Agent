"""
todo.py - Simple CLI todo manager.
"""

import os
import sys

TODOS_FILE = os.path.join(os.path.dirname(__file__), "todos.txt")


def add_todo(item: str):
    """Add a todo item."""
    with open(TODOS_FILE, "a", encoding="utf-8") as f:
        f.write(item + "\n")
    print(f"Added todo: {item}")


def list_todos():
    """List all current todos."""
    if not os.path.exists(TODOS_FILE):
        print("No todos yet.")
        return
    with open(TODOS_FILE, "r", encoding="utf-8") as f:
        todos = [line.strip() for line in f.readlines() if line.strip()]
    if not todos:
        print("No todos yet.")
        return
    print("Todo List:")
    for i, todo in enumerate(todos, start=1):
        print(f"  {i}. {todo}")


def delete_todo(index: int):
    """Delete a todo by 1-based index."""
    if not os.path.exists(TODOS_FILE):
        print("No todos yet.")
        return
    with open(TODOS_FILE, "r", encoding="utf-8") as f:
        todos = [line.strip() for line in f.readlines() if line.strip()]
    if 1 <= index <= len(todos):
        removed = todos.pop(index - 1)
        with open(TODOS_FILE, "w", encoding="utf-8") as f:
            for item in todos:
                f.write(item + "\n")
        print(f"Deleted: {removed}")
    else:
        print(f"Invalid index: {index}. Range is 1 to {len(todos)}.")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "add":
        item = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "New Item"
        add_todo(item)
    elif len(sys.argv) == 2 and sys.argv[1] == "list":
        list_todos()
    elif len(sys.argv) == 3 and sys.argv[1] == "delete":
        try:
            delete_todo(int(sys.argv[2]))
        except ValueError:
            print("Please provide a valid integer index.")
    else:
        print("Usage: python todo.py add <item> | list | delete <index>")
