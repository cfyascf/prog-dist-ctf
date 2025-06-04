from flask import Flask, request, make_response, redirect
import subprocess
import urllib
import os
import re

app = Flask(__name__)

BLACKLIST_PATTERNS = [
    r'\brm\b', r'\brmdir\b'
]

TRAVERSAL_PATTERNS = [
    r'\.\.', r'\.\./', r'\.\.\\', r'%2e%2e', r'%2e%2f', r'%2f%2e', r'\\\.\.', r'/\.\.', r'\bcd\b', r'/'
]

def setup_ctf_dirs():
    dirs = [
        "1d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1",
        "2f8b1e6a-9c8d-4fd1-97b2-5db0cda55d0e-lvl-2",
        "34f7e6a2-9b8c-4e17-82f1-3c5d9bfa2a11-lvl-3"
    ]
    flags = {
        "1d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1": "https://comp-dist-ctf-ahcrhva6dpeff2cb.brazilsouth-01.azurewebsites.net/2f8b1e6a-9c8d-4fd1-97b2-5db0cda55d0e-lvl-2?domain=127.0.0.1",
        "2f8b1e6a-9c8d-4fd1-97b2-5db0cda55d0e-lvl-2": "https://comp-dist-ctf-ahcrhva6dpeff2cb.brazilsouth-01.azurewebsites.net/34f7e6a2-9b8c-4e17-82f1-3c5d9bfa2a11-lvl-3?domain=127.0.0.1",
        "34f7e6a2-9b8c-4e17-82f1-3c5d9bfa2a11-lvl-3": "FLAG${Y0U-R0CK}"
    }
    
    for i, d in enumerate(dirs):
        os.makedirs(d, exist_ok=True)
        flag_path = os.path.join(d, f"flag-{i+1}.txt")
        with open(flag_path, "w") as f:
            f.write(flags[d])

def install_ping():
    subprocess.run(f'apt install iputils-ping -y', shell=True, capture_output=True, text=True)

def is_blocked():
    block_cookie = request.cookies.get("block")
    if block_cookie == "1": return True
    return False

def assign_cookie():
    resp = make_response(redirect("/"))
    resp.set_cookie("block", "1")
    return resp

def is_domain_in_blacklist(domain):
    for pattern in BLACKLIST_PATTERNS:
        if re.search(pattern, domain, flags=re.IGNORECASE):
            return True
    return False

def is_path_traversal(payload):
    decoded = urllib.parse.unquote(payload)
    for pattern in TRAVERSAL_PATTERNS:
        if re.search(pattern, decoded, flags=re.IGNORECASE):
            return True
    return False

def run_rules(domain):
    if is_blocked(): return f"<pre>Seu IP Esta Bloqueado!</pre>"
    if is_domain_in_blacklist(domain): return assign_cookie()
    if is_path_traversal(domain): return f"<pre>Travessia de Diretorio Detectada!</pre>"

@app.route('/')
def home():
    return '''
        <h2>Ping Lab - Command Injection</h2>
        <form action="/1d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1" method="get">
            <input name="domain" value="127.0.0.1" placeholder="Digite o IP 127.0.0.1 ou localhost para começar a pingar">
            <button type="submit">Ping</button>
        </form>
    '''

@app.route('/1d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1', methods=['GET'])
def lvl1():
    domain = request.args.get('domain')
    resp = run_rules(domain)
    if resp is not None: return resp

    try:
        result = subprocess.run(f'cd ./1d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1 && ping -w 2 -c 1 {domain}', shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return f"OUTPUT:<pre>{output}</pre>"
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"
    
@app.route('/2f8b1e6a-9c8d-4fd1-97b2-5db0cda55d0e-lvl-2', methods=['GET'])
def lvl2():
    domain = request.args.get('domain')
    resp = run_rules(domain)
    if resp is not None: return resp
    
    blocked_cmd = [' ',';', '&&', '||']

    for b_cmd in blocked_cmd:
        if b_cmd in domain:
            return f'Erro: Comando nao permitido, tente bypassar esse filtro!'
        
    try:
        result = subprocess.run(f'cd ./2f8b1e6a-9c8d-4fd1-97b2-5db0cda55d0e-lvl-2 && ping -w 2 -c 1 {domain}', shell=True, capture_output=True, text=True)
        output = result.stdout + result.stderr
        return f"OUTPUT:<pre>{output}</pre>"
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

@app.route('/34f7e6a2-9b8c-4e17-82f1-3c5d9bfa2a11-lvl-3', methods=['GET'])
def lvl3():
    domain = request.args.get('domain')
    resp = run_rules(domain)
    if resp is not None: return resp

    blocked_cmd = ['\'', ';', '&&', ' ', '|', '&', '||', 'curl', 'wget']

    for b_cmd in blocked_cmd:
       if b_cmd in domain.lower():
           return f'Erro: Comando nao permitido, tente bypassar esse filtro!'
        
    try:
        result = subprocess.run(f'cd ./34f7e6a2-9b8c-4e17-82f1-3c5d9bfa2a11-lvl-3 && ping -w 2 {domain} -c1', shell=True, capture_output=True, text=True)
        first_line = (result.stdout + result.stderr).strip().split('\n')[0]
        if 'Name or service' in first_line:
            return f"<pre>Safadinho tentou pegar erro, isso aqui nao vai te retornar erros verbosos!</pre>"
        return f"OUTPUT:<pre> Comando Executado: ping {domain} -c1 </pre>\nResult: {first_line}"
    except Exception as e:
        return f"Erro ao executar comando: {str(e)}"

if __name__ == '__main__':
    install_ping()
    setup_ctf_dirs()
    app.run(debug=True)