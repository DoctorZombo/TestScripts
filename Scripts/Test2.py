import socket
from concurrent.futures import ThreadPoolExecutor

#26.169.201.206 / 65535, 1023, -1
ip = '26.246.88.128'

def scan_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        result = s.connect_ex((ip, port))
        if result == 0:
            print(port)

ports = range(0, 65535)

with ThreadPoolExecutor(max_workers=16) as executor:
    executor.map(scan_port, ports)