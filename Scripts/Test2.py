import socket
import os


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(5)
    print("Сервер запущен на http://localhost:8080...")

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode('utf-8')

        # Разделение заголовков и тела запроса
        headers, body = request.split("\r\n\r\n", 1)
        method, path, _ = headers.split("\r\n")[0].split(" ")

        # Обработка GET-запроса для отправки HTML-файла
        if method == "GET":
            if path == "/":  # Главная страница
                filepath = "form.html"  # Файл формы
            else:  # Если пользователь запросил другой файл
                filepath = path.lstrip("/")  # Убираем слэш

            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as file:
                    response_body = file.read()
                response = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "\r\n"
                    f"{response_body}"
                )
            else:
                # Если файл не найден
                response_body = "<h1>404: File Not Found</h1>"
                response = (
                    "HTTP/1.1 404 NOT FOUND\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "\r\n"
                    f"{response_body}"
                )

        # Обработка POST-запроса для получения данных формы
        elif method == "POST":
            content_length = int([line.split(": ")[1] for line in headers.split("\r\n") if "Content-Length" in line][0])
            post_data = body[:content_length]

            # Разбор данных из формы
            form_data = {kv.split("=")[0]: kv.split("=")[1] for kv in post_data.split("&")}
            user_input = form_data.get('user_input', '')

            # Генерация ответа с обработанными данными
            response_body = f"<html><body><h1>Вы ввели: {user_input}</h1></body></html>"
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}"
            )

        # Отправка ответа клиенту
        client_socket.sendall(response.encode('utf-8'))
        client_socket.close()


start_server()
