from math_tools.operations import hamming_encode
import connection_tools.connection as connect

# stage 0 - input
conn, server_socket = connect.start_server()

# Вариант 8: 01010101100
bin_basic_polinom = 0b01010101100 
n = 15
k = 11

# stage 1 - encode (Hamming [15, 11])
# Получаем "эталонное" кодовое слово (15 бит)
bin_encode_polinom = hamming_encode(bin_basic_polinom, k, n)
print(f"Encoded vector (v): {bin(bin_encode_polinom)}")

# stage 2 - set error & send
# Перебираем все возможные вектора ошибок от 1 до 2^n - 1
# Для n=15 это 32767 итераций
conn.send(bin_encode_polinom.to_bytes(2, byteorder='big')) # Сначала отправляем эталон

for i in range(1, 2**n):
    # Накладываем ошибку (XOR)
    bin_wrong_polinom = bin_encode_polinom ^ i
    
    # Отправляем 2 байта (так как 15 бит не влезут в 1 байт)
    binary_data = bin_wrong_polinom.to_bytes(2, byteorder='big')
    conn.send(binary_data)

conn.send(b'END')
connect.connection_termination(conn)
connect.socket_termination(server_socket)