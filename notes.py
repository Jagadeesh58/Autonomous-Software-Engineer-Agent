"""
notes.py - Simple file-based notes utility.
"""

import os

NOTES_FILE = "notes.txt"


def add_note(note: str):
    """Add a note to notes.txt."""
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(note.strip() + "\n")
    print(f"Added note: {note}")


def list_notes():
    """List all notes in notes.txt."""
    if not os.path.exists(NOTES_FILE):
        print("No notes found.")
        return
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        notes = f.readlines()
    if not notes:
        print("No notes found.")
        return
    print("Notes:")
    for idx, note in enumerate(notes, start=1):
        print(f"{idx}. {note.strip()}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        add_note(" ".join(sys.argv[1:]))
    else:
        list_notes()
