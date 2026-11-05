"""Opt-in LAN dashboard. Only bounded derived state is shared, never frame buffers."""
from copy import deepcopy
import ipaddress
import json
from pathlib import Path
import secrets
import socket
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class PhoneBridge:
    def __init__(self):
        self.lock=threading.Lock();self.state={'connected':False};self.report={};self.last_client=0.

    def publish(self,state,report):
        # A JSON round-trip constrains the boundary to structured values, not Qt images/arrays.
        state=json.loads(json.dumps(state,allow_nan=False));report=json.loads(json.dumps(report,allow_nan=False))
        with self.lock:self.state=state;self.report=report

    def read(self,report=False):
        with self.lock:self.last_client=time.monotonic();return deepcopy(self.report if report else self.state)


def local_networks():
    """Label interfaces so a virtual/VPN IP is not mistaken for the Wi-Fi address."""
    import psutil
    found=[];stats=psutil.net_if_stats()
    for name,addresses in psutil.net_if_addrs().items():
        if name in stats and not stats[name].isup:continue
        lower=name.lower()
        virtual=any(x in lower for x in ('vethernet','virtual','vmware','wsl','docker','loopback','tailscale','vpn','wireguard','zerotier','tap-'))
        wireless=any(x in lower for x in ('wi-fi','wifi','wireless','wlan'))
        for addr in addresses:
            if addr.family!=socket.AF_INET:continue
            try:ip=ipaddress.ip_address(addr.address)
            except ValueError:continue
            if ip.is_private and not ip.is_loopback and not ip.is_link_local and not ip.is_unspecified:
                found.append((2 if virtual else 0 if wireless else 1,name,str(ip)))
    return [(name,address) for _,name,address in sorted(set(found))] or [('No LAN address · laptop only','127.0.0.1')]


def local_addresses():return list(dict.fromkeys(address for _,address in local_networks()))


def private_firewall_command(port,executable=None):
    """Copyable, explicit-user-run fix. Never execute or weaken the global firewall."""
    import hashlib
    import ntpath
    import sys
    if type(port) is not int or not 0<port<65536:raise ValueError('Invalid dashboard port')
    executable=str(executable or sys.executable)
    programs=[executable]
    if ntpath.basename(executable).lower() in ('python.exe','pythonw.exe'):
        programs=[ntpath.join(ntpath.dirname(executable),name) for name in ('python.exe','pythonw.exe')]
    quote=lambda value:"'"+value.replace("'","''")+"'"
    lines=[]
    for program in programs:
        name='CheckpointPhone-'+hashlib.sha256((program.lower()+':'+str(port)).encode()).hexdigest()[:16]
        lines.append(f"if (-not (Get-NetFirewallRule -Name {quote(name)} -ErrorAction SilentlyContinue)) {{ New-NetFirewallRule -Name {quote(name)} -DisplayName 'Checkpoint phone dashboard' -Direction Inbound -Action Allow -Enabled True -Protocol TCP -LocalPort {port} -Program {quote(program)} -Profile Private -RemoteAddress LocalSubnet -ErrorAction Stop | Out-Null }}")
    lines.append("Write-Output 'Checkpoint private-network rule is ready. Keep the app open and rescan its QR code.'")
    return '\n'.join(lines)


class PhoneServer:
    def __init__(self,bridge,host='0.0.0.0',port=8765):
        self.bridge=bridge;self.started=0.;self.last_page_request=0.;self.token=secrets.token_urlsafe(24);self.server=None;self.thread=None;self.host=host;self.port=port

    def start(self):
        owner=self;assets=Path(__file__).with_name('assets')
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def setup(self):
                super().setup();self.connection.settimeout(3)
            def send_data(self,status,data,kind='application/json'):
                if not isinstance(data,bytes):data=json.dumps(data,allow_nan=False).encode('utf8')
                self.send_response(status);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(data)))
                self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
                self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; frame-ancestors 'none'")
                if self.path=='/api/report':self.send_header('Content-Disposition','attachment; filename="checkpoint-session.json"')
                self.end_headers();self.wfile.write(data)
            def do_GET(self):
                if self.path=='/favicon.ico':return self.send_data(204,b'','image/png')
                if self.path=='/':
                    owner.last_page_request=time.monotonic()
                    return self.send_data(200,(assets/'phone.html').read_bytes(),'text/html; charset=utf-8')
                if self.path=='/font.ttf':return self.send_data(200,(assets/'DM-Sans.ttf').read_bytes(),'font/ttf')
                if self.path not in ('/api/state','/api/report'):return self.send_data(404,{'error':'Not found'})
                auth=self.headers.get('Authorization','')
                if not auth.isascii() or not secrets.compare_digest(auth,'Bearer '+owner.token):return self.send_data(401,{'error':'Pair with the link from your laptop'})
                return self.send_data(200,owner.bridge.read(report=self.path=='/api/report'))
        class Server(ThreadingHTTPServer):
            daemon_threads=True
            allow_reuse_address=True
        try:self.server=Server((self.host,self.port),Handler)
        except OSError:
            if not self.port:raise
            self.server=Server((self.host,0),Handler)
        self.port=self.server.server_address[1];self.started=time.monotonic()
        self.thread=threading.Thread(target=self.server.serve_forever,kwargs={'poll_interval':.15},daemon=True);self.thread.start();return self

    def url(self,address):return f'http://{address}:{self.port}/#pair={self.token}'

    def stop(self):
        if self.server:self.server.shutdown();self.server.server_close();self.server=None
        if self.thread:self.thread.join(timeout=2);self.thread=None
        self.token=secrets.token_urlsafe(24)
