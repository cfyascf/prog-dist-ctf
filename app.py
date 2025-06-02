from flask import Flask, request
import subprocess

app = Flask(__name__)
ip_blacklist = []
WORD_BLACKLIST = ['RM', 'rm', 'RMDIR', 'rmdir']

def get_real_ip():
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        ip_port = forwarded.split(',')[0].strip()
        ip = ip_port.split(':')[0]
        return ip
    return None
    
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
            <input name="domain" placeholder="Digite um IP ou hostname">
            <button type="submit">Ping</button>
        </form>
    '''

@app.route('/5d8f3d1a-b55b-4d23-b1cd-fd3d1e8a67e9-lvl-1', methods=['GET'])
def lvl1():
    ip = get_real_ip()
    if is_ip_blocked(ip): return f"<pre>Your IP {ip} is blocked</pre>"

    domain = request.args.get('domain')

    if is_host_in_blacklist(domain):
        block_ip(ip)
        return f"<pre>Your IP {ip} is blocked/pre>"


    result = subprocess.run(f'ping -c 1 {domain}', shell=True, capture_output=True, text=True)
    output = result.stdout + result.stderr
    return f"OUTPUT:<pre>{output}</pre>"

if __name__ == '__main__':
    app.run(debug=True)