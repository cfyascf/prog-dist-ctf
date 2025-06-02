from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/lvl-1', methods=['GET'])
def execute_command_1():
    domain = request.args.get('domain')
    if not '.' in domain:
        return f"Erro: Isso nao eh um dominio"
    try:
        result = subprocess.run(f'netstat {domain}', shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return f"OUTPUT:<pre>{output}</pre>"
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

@app.route('/lvl-2', methods=['GET'])
def execute_command_2():
    domain = request.args.get('domain')
    blocked_cmd = ['127.0.0.1', '192.168.1.254',' ',';', '&&', '||']
    if not '.' in domain:
        return f"Erro: Isso nao eh um dominio"
    for b_cmd in blocked_cmd:
        if b_cmd in domain:
            return f'Erro: Comando nao permitido'
    try:
        result = subprocess.run(f'netstat {domain}', shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return f"OUTPUT:<pre>{output}</pre>"
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

@app.route('/lvl-3', methods=['GET'])
def execute_command_3():
    domain = request.args.get('domain')
    blocked_cmd = ['127.0.0.1', '192.168.1.254','\'', 'curl', 'webhook', ';', '&&', ' ', '|', '&', '||']
    if not '.' in domain:
        return f"Erro: Isso nao eh um dominio"
    for b_cmd in blocked_cmd:
        if b_cmd in domain:
            return f'Erro: Comando nao permitido'
    try:
        result = subprocess.run(f'ping {domain} -c1', shell=True, capture_output=True, text=True)
        first_line = (result.stdout + result.stderr).strip().split('\n')[0]
        if 'Name or service' in first_line:
            return f"<pre>Safadinho tentou pegar erro verboso ne, vai trabaia</pre>"
        return f"OUTPUT:<pre> Comando Executado: ping {domain} -c1</pre>\nResult: {first_line}"
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
