from tabulate import tabulate

"""
Выполнил: Снежко Максим, группа 253505
Вариант 20
Задание 1
Разложение функции в степенной ряд
02.03.2024
"""
def get_input_values():
    """
    Получает значения аргумента x и точности epsilon от пользователя.
    Проверяет их на правильность ввода и возвращает их.
    Если значение аргумента x находится за пределами допустимого интервала (-1 < x < 1), 
    функция выводит сообщение об ошибке и требует повторный вввод данных.
    Если значение точности epsilon отрицательное, функция также выводит сообщение об ошибке и требует повторный вввод данных.
    """
    while True:
        try:
            x = float(input("Введите значение аргумента x (-1 < x < 1): "))
            if x <= -1 or x >= 1:
                print("Недопустимый аргумент")
                continue
            epsilon = float(input("Введите желаемую точность вычислений epsilon: "))
            if epsilon < 0:
                print("Значение должно быть > 0")
                continue
        except ValueError:
            print("Ошибка ввода")
            continue
        return x, epsilon

def calculate_function(x, epsilon):
    """
    Выполняет разложение функции в степенной ряд для заданных значения аргумента x и точности epsilon.
    Выводит результат разложения функции, точность и количество членов ряда, необходимых для достижения указанной точности.
    
    Цикл выполяется, пока на какой-то итерации значении переменной degree будет меньше значения epsilon либо когда не 
    будет достигнуто 500 итераций
    """
    result, n = 0, 0
    math_result = 1 / (1 - x)   
    while True:
        degree = x ** n
        n += 1
        if abs(degree) < epsilon or n > 499:
            break            
        result += degree
    data = [[x, n, result, math_result, epsilon]]
    headers = ["x", "n", "F(x)", "Math F(x)", "eps"]
    print(tabulate(data, headers=headers, tablefmt="grid"))
    
    
def task1():
    print(calculate_function.__doc__)
    x, epsilon = get_input_values()
    calculate_function(x, epsilon)