def get_hamming_control_bits_indices(n):
    """Возвращает список позиций контрольных бит (1, 2, 4, 8...) <= n"""
    indices = []
    i = 1
    while i <= n:
        indices.append(i)
        i *= 2
    return indices

def hamming_encode(data_int, k, n):
    """
    Кодирование кодом Хэмминга.
    data_int: информационное слово (число)
    k: число инфо бит
    n: общее число бит
    """
    # 1. Расставляем информационные биты по своим местам
    # Контрольные биты занимают позиции 1, 2, 4, 8...
    # Информационные занимают остальные (3, 5, 6, 7, 9...)
    encoded = 0
    control_indices = get_hamming_control_bits_indices(n)
    
    # Итератор по битам данных (справа налево, от младшего к старшему)
    data_bit_pos = 0 
    
    # Проходим по всем позициям кодового слова от 1 до n
    for i in range(1, n + 1):
        if i in control_indices:
            continue # Пропускаем места под контрольные биты
        
        # Берем бит из данных
        bit = (data_int >> data_bit_pos) & 1
        data_bit_pos += 1
        
        # Ставим его на позицию i (в числе бит i-1, т.к. индексация с 0)
        if bit:
            encoded |= (1 << (i - 1))
            
    # 2. Вычисляем значения контрольных бит
    # Значение контрольного бита P_j = XOR сумма битов на позициях, 
    # в двоичном представлении которых есть j
    for p in control_indices:
        # p - это позиция (1, 2, 4, 8). 
        parity = 0
        for i in range(1, n + 1):
            # Если на позиции i стоит 1 И эта позиция контролируется битом p
            if (encoded >> (i - 1)) & 1:
                # Проверка вхождения: i имеет бит p (побитовое И)
                if (i & p):
                    parity ^= 1
        
        # Если четность 1, выставляем контрольный бит
        if parity:
            encoded |= (1 << (p - 1))
            
    return encoded

def hamming_decode_correction(received_int, n):
    """
    Декодирование и исправление ошибки.
    Возвращает (исправленное_слово, синдром).
    """
    syndrome = 0
    
    # Вычисление синдрома: XOR позиций всех единичных битов
    for i in range(1, n + 1):
        bit = (received_int >> (i - 1)) & 1
        if bit:
            syndrome ^= i
            
    corrected_int = received_int
    
    # Если синдром != 0 и указывает на валидную позицию, инвертируем бит
    if 0 < syndrome <= n:
        # Инверсия бита на позиции syndrome (индекс syndrome-1)
        corrected_int ^= (1 << (syndrome - 1))
        
    return corrected_int, syndrome