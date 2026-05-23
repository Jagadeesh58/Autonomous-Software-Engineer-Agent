import os

todos_file = 'todos.txt'

def add_todo(item):
    with open(todos_file, 'a') as f:
        f.write(item + '\n')

def list_todos():
    try:
        with open(todos_file, 'r') as f:
            todos = f.readlines()
            for i, todo in enumerate(todos):
                print(f'{i+1}. {todo.strip()}')
    except FileNotFoundError:
        print('No todos yet.')

def delete_todo(index):
    try:
        with open(todos_file, 'r') as f:
            todos = f.readlines()
        if index > 0 and index <= len(todos):
            todos.pop(index-1)
            with open(todos_file, 'w') as f:
                f.writelines(todos)
        else:
            print('Invalid index.')
    except FileNotFoundError:
        print('No todos yet.')

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2 and sys.argv[1] == 'add':
        add_todo('Item to add')
    elif len(sys.argv) == 2 and sys.argv[1] == 'list':
        list_todos()
    elif len(sys.argv) == 3 and sys.argv[1] == 'delete':
        delete_todo(int(sys.argv[2]))
    else:
        print('Usage: python todo.py add|list|delete <index>')