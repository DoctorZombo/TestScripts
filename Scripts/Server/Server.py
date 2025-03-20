import socket
import os
import sys
import ssl

def resource_path(relative_path):
    """Получить путь к ресурсу, учитывая запуск из EXE."""
    if hasattr(sys, '_MEIPASS'):  # Проверяет, если запуск идёт из EXE
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
cert_path = resource_path('certificate/server.crt')
key_path = resource_path('certificate/server.key')
def start_server():
    # Создаем базовый сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('0.0.0.0', 25564))
    sock.listen(5)

    # Настройка TLS-контекста

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=cert_path, keyfile=key_path)



    # Обертывание сокета в TLS
    tls_sock = context.wrap_socket(sock, server_side=True)

    print('Сервер запущен')

    while True:
        try:
            client_socket, address = tls_sock.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            headers, body = data.split('\r\n\r\n', 1)
            method, path, _ = headers.split('\r\n')[0].split(' ')
            content = loag_page(method, path)
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
            client_socket.close()
        except Exception as e:
            print(e)

def loag_page(method, path):
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    print(path)
    if method == 'GET':
        try:
            file_path = resource_path('views' + path + '.html')
            with open(file_path, 'rb') as file:
                responce = file.read()
            return HDRS.encode('utf-8') + responce
        except FileNotFoundError:
            return (HDRS_404 + 'No file').encode('utf-8')

if __name__ == '__main__':
    start_server()

    #pyinstaller --onefile --add-data "server/views/*;views" --add-data "server/views/images/*;images" --add-data "server/certificate/*;certificate" server/server.py