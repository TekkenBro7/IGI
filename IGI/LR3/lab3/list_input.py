import random
"""
Выполнил: Снежко Максим, группа 253505
Вариант 20
Функции для ввода списка
02.03.2024
"""

def input_list_choice(func):
    """ Декоратор """
    def wrapper():
        while True:
            print("Как вы хотите ввести список?\n1 - Ввести в строку числа\n2 - ввести количество чисел, а потом по числу\n3 - через функцию автоматического генерирования\n4 - функция генератор")
            try:
                num = int(input("Введите число от 1 до 4: "))
                if num not in [1, 2, 3, 4]:
                    raise ValueError("Неправильный ввод. Пожалуйста, введите число от 1 до 3.")
                func(num)
                break
            except ValueError:
                print("Ошибка ввода")
                continue
    return wrapper

def input_list_by_count():
    """ Функция для ввода элементов списка пользователем по заданному количеству. """
    while True:
        try:
            num = int(input("Введите количество элементов в списке: "))
            if num <= 0:
                print("Количество элементов должно быть положительным числом.")
                continue
            float_list = []
            for i in range(num):
                float_list.append(float(input(f"Введите {i + 1} элемент: ")))
            return float_list
        except ValueError:
            print("Ошибка ввода, повторите по ввод")
            continue
 
def input_list():
    """ Функция для ввода элементов списка пользователем через строку чисел. """
    while True:
        try:
            elements = input("Введите элементы списка через пробел: ")
            float_list = [float(element) for element in elements.split()]
            return float_list
        except ValueError:
            print("Ошибка ввода. Пожалуйста, введите только вещественные числа.")
            continue 
        
def generate_random_list(size):
    """ Функция для генерации случайного списка вещественных чисел заданного размера. """
    return [random.uniform(-100, 100) for _ in range(size)]

def simple_generator(left = 0, right = 10):
    """ Функция генератора. """
    i = left
    while i <= right:
        yield i
        i += 1