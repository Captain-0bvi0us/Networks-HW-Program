from display_tools.display import draw_table_corrected
from math_tools.operations import hamming_decode_correction
import connection_tools.connection as connect

# stage 0
conn = connect.start_client()
n = 15 # Важно: 15 для кода Хэмминга [15,11]

# Сначала получаем эталон
data = conn.recv(2)
bin_encode_polinom = int.from_bytes(data, byteorder='big')
print(f"Reference Code Vector received: {bin(bin_encode_polinom)}")

# Статистика
corrected_errors = [0] * n        # Nk - исправленные
found_errors_count = [0] * n      # No - обнаруженные (синдром != 0)
total_errors_by_weight = [0] * n  # C(n,i) - всего ошибок

iteration = 1
max_iter = 2**n # 32768

while True:
    # Прием данных (2 байта)
    data = conn.recv(2)
    
    if not data or data == b'END' or iteration >= max_iter:
        break
    
    bin_received_polinom = int.from_bytes(data, byteorder='big')

    # 1. Определяем реальную кратность ошибки для статистики (C(n,i))
    real_error_vector = bin_received_polinom ^ bin_encode_polinom
    error_weight = bin(real_error_vector).count('1')
    
    if error_weight > 0:
        total_errors_by_weight[error_weight - 1] += 1

    # 2. Декодирование (процесс обнаружения и исправления)
    bin_corrected_polinom, syndrome = hamming_decode_correction(bin_received_polinom, n)
    
    # Если синдром != 0, значит декодер ОБНАРУЖИЛ ошибку (No)
    if syndrome != 0 and error_weight > 0:
        found_errors_count[error_weight - 1] += 1
    
    # 3. Проверка результата (Nk)
    # Если после работы декодера вектор совпал с исходным эталоном
    if bin_corrected_polinom == bin_encode_polinom and error_weight > 0:
        corrected_errors[error_weight - 1] += 1

    iteration += 1

# Вывод таблицы с новыми аргументами
# Передаем: n, Всего, Обнаружено(No), Исправлено(Nk)
draw_table_corrected(n, total_errors_by_weight, found_errors_count, corrected_errors)

connect.socket_termination(conn)