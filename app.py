from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    return 'Hello World'

@app.route('/add')
def add():
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    return str(a + b)
