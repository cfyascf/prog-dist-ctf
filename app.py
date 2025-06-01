from flask import Flask, request
import subprocess

app = Flask(__name__)
ip_blacklist = []
WORD_BLACKLIST = ['RM', 'rm', 'RMDIR', 'rmdir']


def is_host_in_blacklist(host):
    if any(e in host for e in WORD_BLACKLIST):
        return True

def block_ip(ip):
    ip_blacklist.append(ip)

def is_ip_blocked(ip):
    if ip in ip_blacklist:
        return True

@app.route('/')
def home():
    return '''
        <h2>Ping Lab - Command Injection</h2>
        <form action="/5d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1" method="get">
            <input name="host" placeholder="Digite um IP ou hostname">
            <button type="submit">Ping</button>
        </form>
    '''

@app.route('/5d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1', methods=['GET'])
def lvl1():
    ip = request.remote_addr
    if is_ip_blocked(ip): return f"<pre>Your IP is blocked, get out now</pre>"

    host = request.args.get('host')
    if is_host_in_blacklist(host):
        block_ip(ip)
        return f"<pre>Your IP {ip} is blocked, get out now</pre>"
    command = f"ping -c 2 {host}"

    try:
        result = subprocess.check_output(command, shell=True, text=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        result = f"Erro ao executar o comando:\n{e.output}"

    return f"<pre>{result}</pre>"

if __name__ == '__main__':
    app.run(debug=True)