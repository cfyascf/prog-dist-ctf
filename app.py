# app.py
from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
        <h2>Ping Lab - Command Injection</h2>
        <form action="/ping" method="post">
            <input name="host" placeholder="Digite um IP ou hostname">
            <button type="submit">Ping</button>
        </form>
    '''

@app.route('/ping', methods=['POST'])
def ping():
    host = request.form.get('host')
    command = f"ping -c 2 {host}"
    result = os.popen(command).read()
    return f"<pre>{result}</pre>"
    
if __name__ == '__main__':
    app.run(debug=True)