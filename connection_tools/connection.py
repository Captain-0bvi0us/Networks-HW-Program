import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))
    
    # Приветствие (можно оставить для проверки связи)
    data = client_socket.recv(1024)
    # print(f"Log: {data.decode()}")
    client_socket.send(b"ready")
    return client_socket

def socket_termination(client_socket):
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Опция REUSEADDR позволяет быстро перезапускать сервер без ошибки "Address already in use"
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Сервер запущен (Вариант 8: Хэмминг [15,11])...")
    
    conn, addr = server_socket.accept()
    print(f"Клиент подключен: {addr}")
    
    conn.send(b"Server Ready")
    conn.recv(1024) # Ждем ready от клиента
    return conn, server_socket

def connection_termination(conn): 
    conn.close()