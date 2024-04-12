import matplotlib.colors as mcolors

def validate_positive_float(text):
    """
    Проверяет, является ли введенное значение положительным числом типа float.
    """
    while True:
        try:
            float_value = float(input(text))
            if float_value > 0:
                return float_value
            else:
                print("Введите положительное число: ")
        except ValueError:
            print("Некорректный ввод, введите число повторно!")

def validate_positive_int(text):
    """
    Проверяет, является ли введенное значение положительным числом типа int.
    """
    while True:
        try:
            float_value = int(input(text))
            if float_value > 0:
                return float_value
            else:
                print("Введите положительное число: ")
        except ValueError:
            print("Некорректный ввод, введите число повторно!")

def validate_angle(angle):
    """
    Проверяет, является ли введенное значение углом, не кратным 180 и 360.
    """
    while True:
        try:
            float_value = float(input(angle))
            if float_value % 180 != 0 and float_value % 360 != 0:
                return float_value
            else:
                print("Введите число не кратное 180 и 360!")
        except ValueError:
            print("Некорректный ввод, введите число повторно!")
            
            
def input_existing_color(text):
    """
    Проверяет, является ли указанный цвет существуюшим или нет
    """
    while True:
        try:
            color = input(text)
            if mcolors.to_rgba(color):
                return color               
        except ValueError:
            print("Цвет не существует. Пожалуйста, введите верный цвет.")
            continue