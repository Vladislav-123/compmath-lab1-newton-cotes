import math
import matplotlib.pyplot as plt
from quadrature import midpoint, trapezoidal, simpson, three_eights
from test_functions import f1, f1_exact, f2, f2_exact, f3, f3_exact, f4, f4_exact
from error_analysis import absolute_error, convergence_rate

# Эксперимент 1: Зависимость числа узлов от требуемой точности
def experiment_precision():
    print('\nЭксперимент 1: Влияние точности на число узлов')
    a, b = 0.0, 1.0
    exact = f1_exact(a, b) # точное значение для f1(x)=e^x
    M2 = math.exp(1) # max |f''| на [0,1] для e^x
    M4 = math.exp(1) # max |f^(4)|

    epsilons = [1e-3, 1e-4, 1e-5, 1e-6, 1e-7]

    # Заголовок таблицы
    header = f"{'epsilon':<10} {'Прямоугольники':<20} {'Трапеции':<20} {'Симпсон':<20} {'3/8':<20}"
    print(header)
    print('-' * 90)

    for eps in epsilons:
        # Прямоугольники: |R| <= (b-a)*h^2/24 * M2
        h_rect = math.sqrt(24 * eps / ((b-a) * M2))
        n_rect = int(math.ceil((b-a) / h_rect))
        I_rect = midpoint(f1, a, b, n_rect)
        err_rect = absolute_error(I_rect, exact)
        while err_rect > eps:
            n_rect += 1
            I_rect = midpoint(f1, a, b, n_rect)
            err_rect = absolute_error(I_rect, exact)

        # Трапеции: |R| <= (b-a)*h^2/12 * M2
        h_trap = math.sqrt(12 * eps / ((b-a) * M2))
        n_trap = int(math.ceil((b-a) / h_trap))
        I_trap = trapezoidal(f1, a, b, n_trap)
        err_trap = absolute_error(I_trap, exact)
        while err_trap > eps:
            n_trap += 1
            I_trap = trapezoidal(f1, a, b, n_trap)
            err_trap = absolute_error(I_trap, exact)

        # Симпсон: |R| <= (b-a)*h^4/180 * M4
        h_simp = (180 * eps / ((b-a) * M4)) ** 0.25
        n_simp = int(math.ceil((b-a) / h_simp))
        if n_simp % 2 != 0:
            n_simp += 1 # делаем чётным
        I_simp = simpson(f1, a, b, n_simp)
        err_simp = absolute_error(I_simp, exact)
        while err_simp > eps:
            n_simp += 2
            I_simp = simpson(f1, a, b, n_simp)
            err_simp = absolute_error(I_simp, exact)

        # Три восьмых: |R| <= 3*(b-a)*h^4/80 * M4
        h_38 = (80 * eps / (3 * (b-a) * M4)) ** 0.25
        n_38 = int(math.ceil((b-a) / h_38))
        if n_38 % 3 != 0:
            n_38 = ((n_38 + 2) // 3) * 3 # делаем кратным трём
        I_38 = three_eights(f1, a, b, n_38)
        err_38 = absolute_error(I_38, exact)
        while err_38 > eps:
            n_38 += 3
            I_38 = three_eights(f1, a, b, n_38)
            err_38 = absolute_error(I_38, exact)

        # Вывод строки таблицы
        row = f"{eps:<10.0e} {n_rect:<20} {n_trap:<20} {n_simp:<20} {n_38:<20}"
        print(row)


# Эксперимент 2: Влияние гладкости функции
def experiment_smoothness():
    print('\nЭксперимент 2: Влияние гладкости функции')

    # Набор функций и отрезков
    functions = [
        (f1, f1_exact, (0,1), 'e^x'),
        (f2, f2_exact, (0,1), 'x^3'),
        (f3, f3_exact, (0,1), 'sqrt(x)'),
        (f4, f4_exact, (-1,1), '1/(1+25x^2)')
    ]

    n_values = [6, 12, 24, 48, 96, 192] # Значения кратны трем

    # Для каждого метода собираем данные для построения графиков
    methods = [
        ('Прямоугольники', midpoint),
        ('Трапеции', trapezoidal),
        ('Симпсон', simpson),
        ('3/8', three_eights)
    ]

    # Для каждой функции построим отдельный рисунок с четырьмя кривыми
    for func, exact_func, (a,b), name in functions:
        exact = exact_func(a, b)
        plt.figure(figsize=(8,6))

        for method_name, method in methods:
            errors = []
            h_vals = []
            for n in n_values:
                try:
                    val = method(func, a, b, n)
                except ValueError:
                    # Метод не применим (например, n нечётное для Симпсона или не кратно 3)
                    continue
                except Exception as e:
                    # Ловим любые другие неожиданные ошибки
                    print(f'Неожиданная ошибка для {method_name}, {name}, n={n}: {e}')
                    continue
                # Проверка типа на всякий случай
                if not isinstance(val, (int, float)):
                    print(f'Предупреждение: {method_name} вернул {type(val)} для n={n}')
                    continue
                err = absolute_error(val, exact)
                h = (b - a) / n
                errors.append(err)
                h_vals.append(h)
            if errors:
                plt.loglog(h_vals, errors, 'o-', label=method_name)

        plt.xlabel('Шаг h')
        plt.ylabel('Абсолютная погрешность')
        plt.title(f'Сходимость для функции {name}')
        plt.legend()
        plt.grid(True, which='both', ls='--', alpha=0.7)
        # Заменяем слеш в имени файла, чтобы избежать проблем с путями
        safe_name = name.replace('/', '_').replace('\\', '_')
        plt.savefig(f'convergence_{safe_name}.png', dpi=150)
        plt.close()
        print(f'График для {name} сохранён')

    # Дополнительно вычислим порядок сходимости для каждой пары (функция, метод)
    print('\nОценка порядка сходимости (по последним двум точкам):')
    for func, exact_func, (a,b), name in functions:
        exact = exact_func(a, b)
        for method_name, method in methods:
            errors = []
            h_vals = []
            for n in n_values:
                try:
                    val = method(func, a, b, n)
                except ValueError:
                    continue
                except Exception:
                    continue
                if not isinstance(val, (int, float)):
                    continue
                err = absolute_error(val, exact)
                h = (b - a) / n
                errors.append(err)
                h_vals.append(h)
            if len(errors) >= 2:
                p = convergence_rate(errors, h_vals)
                if p is not None:
                    print(f'{name:20} {method_name:15} : p ~ {p:.2f}')
                else:
                    print(f'{name:20} {method_name:15} : не удалось оценить')


# Эксперимент 3: Сравнение теоретической и фактической погрешности
def experiment_theoretical_vs_actual():
    print('\nЭксперимент 3: Сравнение теоретической и фактической погрешности')
    a, b = 0.0, 1.0
    exact = f1_exact(a, b)
    M2 = math.exp(1)
    M4 = math.exp(1)

    n_values = [6, 12, 24, 48, 96, 192] # Значения кратны трем
    methods_info = [
        ('Прямоугольники', midpoint, lambda h: (b-a) * h**2/24 * M2),
        ('Трапеции', trapezoidal, lambda h: (b-a) * h**2/12 * M2),
        ('Симпсон', simpson, lambda h: (b-a) * h**4/180 * M4),
        ('3/8', three_eights, lambda h: 3 * (b-a) * h**4/80 * M4)
    ]

    plt.figure(figsize=(10,8))

    for method_name, method, theo_func in methods_info:
        h_vals = []
        err_actual = []
        err_theo = []
        for n in n_values:
            try:
                val = method(f1, a, b, n)
            except ValueError:
                continue
            if not isinstance(val, (int, float)):
                continue
            h = (b - a) / n
            err_actual.append(absolute_error(val, exact))
            err_theo.append(theo_func(h))
            h_vals.append(h)
        plt.loglog(h_vals, err_actual, 'o-', label=f'{method_name} (факт)')
        plt.loglog(h_vals, err_theo, 's--', label=f'{method_name} (теория)')

    plt.xlabel('Шаг h')
    plt.ylabel('Погрешность')
    plt.title('Сравнение фактической и теоретической погрешности для e^x')
    plt.legend()
    plt.grid(True, which='both', ls='--', alpha=0.7)
    plt.savefig('theoretical_vs_actual.png', dpi=150)
    plt.close()
    print('График theoretical_vs_actual.png сохранён')


if __name__ == '__main__':
    experiment_precision()
    experiment_smoothness()
    experiment_theoretical_vs_actual()
    print('\nВсе эксперименты завершены')
