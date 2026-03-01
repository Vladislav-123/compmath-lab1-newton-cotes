# Функция для анализа погрешностей

import math

def absolute_error(approx, exact):
    '''Возвращается абсолютную погрешность'''
    return abs(approx - exact)

def convergence_rate(errors, h_values):
    '''
    Оценивает порядок сходимости по двум последним точкам
    errors – список абсолютных погрешностей
    h_values – соответствующие значения шага
    Возвращает оценку порядка p или None, если данных недостаточно
    '''
    if len(errors) < 2 or len(h_values) < 2:
        return None
    # Используем последние два значения для оценки
    e1, e2 = errors[-2], errors[-1]
    h1, h2 = h_values[-2], h_values[-1]
    if e1 == 0 or e2 == 0:
        return None
    return math.log(e1/e2) / math.log(h1/h2)
