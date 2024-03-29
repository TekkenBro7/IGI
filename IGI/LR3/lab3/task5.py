from list_input import *
"""
Выполнил: Снежко Максим, группа 253505
Вариант 20
Задание 5
Найти максимальный по модулю элемент списка и сумму элементов списка, 
расположенных между первым и вторым отрицательными элементами
02.03.2024
"""

def find_max_abs_sum_between_negatives(float_list):
    """
    Функция для поиска максимального по модулю элемента списка
    и суммы элементов списка, расположенных между первым и вторым отрицательными элементами.
    
    Данная функция ищет два отрицательных числа в списке float_list. Если они найдены,
    то функция выводит на экран максимальное по модулю значение между этими числами и сумму 
    чисел между ними. Если в списке нет двух отрицательных чисел, выводится сообщение о несоответствии условию.
    """
    max_abs_value = None
    sum_between_negatives = 0
    first_negative_found = False
    for num in float_list:
        if num < 0:
            if not first_negative_found:
                first_negative_found = True
            else:
                print("Максимальное по модулю значение между двумя отрицательными числами:", max_abs_value)
                print("Сумма между ними:", sum_between_negatives)
                break
        elif first_negative_found:
            sum_between_negatives += num
            if max_abs_value is None or abs(num) > abs(max_abs_value):
                max_abs_value = num 
    else:
        print("Не выполнилось необходимое условие: нет двух отрицательных чисел в списке")

@input_list_choice
def task5(choice):
    """ Основная функция программы для решения задачи 5. """
    if choice == 1:
        float_list = input_list()
    elif choice == 2:
        float_list = input_list_by_count()
    elif choice == 3:
        count = int(input("Введите количество чисел: "))
        float_list = generate_random_list(count)
    elif choice == 4:
        min_num = int(input("Введите минимальное число: "))
        max_num = int(input("Введите максимальное число: "))
        float_list = list(simple_generator(min_num, max_num))
    print("Список введенных чисел:", *float_list)
    find_max_abs_sum_between_negatives(float_list)