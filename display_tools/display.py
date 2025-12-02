import math

def drawLine():
    # Увеличили ширину разделителя для новой колонки
    print('+-----+---------+---------+---------+-----------+')

def draw_table_corrected(n, total_errors, detected_count, corrected_count):
    # Шапка таблицы: i | C(n,i) | No | Nk | Ck
    drawLine()
    print('| {:>3} | {:>7} | {:>7} | {:>7} | {:>9} |'.format('i', 'C(n,i)', 'No', 'Nk', 'Ck'))
    drawLine()
    
    for i in range(n):
        # i+1 - это кратность ошибки
        total = total_errors[i]      # Всего ошибок (C из n по i)
        detected = detected_count[i] # Обнаружено (синдром != 0)
        corrected = corrected_count[i] # Исправлено (совпало с эталоном)
        
        # Расчет коэффициента Ck
        if total > 0:
            ck_val = corrected / total
        else:
            ck_val = 0.0
            
        print('| {:>3} | {:>7} | {:>7} | {:>7} | {:>9.3f} |'.format(
            i + 1,
            total,
            detected,
            corrected,
            ck_val
        ))
        
    drawLine()