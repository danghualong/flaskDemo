from flask import Flask

app=Flask(__name__)

@app.route('/sy')
def say():
    return '<h1>Hello</h1>'