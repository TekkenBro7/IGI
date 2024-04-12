"""
Выполнил: Снежко Максим Андреевич, группа 253505
Вариант 20
Задание 4
Исследовать возможности библиотека NumPy при работе с массивами и математическими и статическими 
операциями. Сформировать целочисленную матрицу А[n,m] с помощью генератора случайных чисел (random).
а) Библиотека NumPy.
1. Создание массива. Функции array() и values().
2. Функции создания массива заданного вида.
3. Индексирование массивов NumPy. Индекс и срез.
4. Операции с массивами. Универсальные (поэлементные) функции.
б) Математические и статистические операции.
1. Функция mean()
2. Функция median()
3. Функция corrcoef()
4. Дисперсия var().
5. Стандартное отклонение std()
Определить, сколько элементов среди всех элементов матрицы равны минимальному значению. Вывести их 
индексы. Вычислить стандартное отклонение для всех значений матрицы. Ответ округлите до сотых. 
Вычисление стандартного отклонения выполнить двумя способами: через стандартную функцию и через 
программирование формулы.
"""
import numpy as np
import correct_input

class NumPyOperations:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.matrix = None
    
    def __str__(self):
        if self.matrix is not None:
            return f"Количество строк: {self.n}, количество столбцов: {self.m}.\nИсходная матрица:\n{self.matrix}"
        else:
            return f"Матрица еще не создана."
    
    def create_matrix(self, min=0, max=100):
        self.matrix = np.random.randint(min, max, size=(self.n, self.m))    
        
    def create_zeros(self):
        self.matrix = np.zeros((self.n, self.m))
    
    def create_ones(self):
        self.matrix = np.ones((self.n, self.m))
    
    def create_full(self, value):
        self.matrix = np.full((self.n, self.m), value)
        
    def create_eye(self):
        self.matrix = np.eye(self.n)
    
    def create_arange(self, start, stop, step=1):
        self.matrix = np.arange(start, stop, step)
    
    def __getitem__(self, index):
        return self.matrix[index]
    
    def __setitem__(self, index, value):
        self.matrix[index] = value

    def __add__(self, other):
        result = NumPyOperations(self.n, self.m)
        if isinstance(other, NumPyOperations):
            result.matrix = self.matrix + other.matrix
        elif isinstance(other, (int, float)):
            result.matrix = self.matrix + other
        else:
            print("Неподдерживаемый тип операнда для сложения.")
            return self.matrix
        return result
    
    def __sub__(self, other):
        result = NumPyOperations(self.n, self.m)
        if isinstance(other, NumPyOperations):
            result.matrix = self.matrix - other.matrix
        elif isinstance(other, (int, float)):
            result.matrix = self.matrix - other
        else:
            print("Неподдерживаемый тип операнда для вычитания.")
            return self.matrix
        return result
    
    def __mul__(self, other):
        result = NumPyOperations(self.n, self.m)
        if isinstance(other, NumPyOperations):
            result.matrix = self.matrix * other.matrix
        elif isinstance(other, (int, float)):
            result.matrix = self.matrix * other
        else:
            print("Неподдерживаемый тип операнда для умножения.")
            return self.matrix
        return result
    
    def __truediv__(self, other):
        result = NumPyOperations(self.n, self.m)
        if isinstance(other, NumPyOperations):
            result.matrix = self.matrix / other.matrix
        elif isinstance(other, (int, float)):
            result.matrix = self.matrix / other
        else:
            print("Неподдерживаемый тип операнда для деления.")
            return self.matrix
        return result

    def __pow__(self, other):
        result = NumPyOperations(self.n, self.m)
        if isinstance(other, NumPyOperations):
            result.matrix = np.power(self.matrix, other.matrix)
        elif isinstance(other, (int, float)):
            result.matrix = np.power(self.matrix, other)
        else:
            print("Неподдерживаемый тип операнда для возведения в степень.")
            return self.matrix
        return result

    def sqrt(self):
        result = NumPyOperations(self.n, self.m)
        result.matrix = np.sqrt(self.matrix)
        return result

    def abs(self):
        result = NumPyOperations(self.n, self.m)
        result.matrix = np.abs(self.matrix)
        return result 
        
class MatrixStatistics(NumPyOperations):
    def __init__(self, n, m):
        super().__init__(n, m)
        
    def mean(self):
        return np.mean(self.matrix)
    
    def median(self):
        return np.median(self.matrix)
    
    def corrcoef(self):
        return np.corrcoef(self.matrix) 
    
    def var(self):
        return np.var(self.matrix)
    
    def std(self):
        return np.std(self.matrix)
     
    def sort_last_row(self):
        self.matrix[-1, :] = np.sort(self.matrix[-1, :])
        
    def median_last_row(self):
        return np.median(self.matrix[-1, :])
    
    def individual_median_last_row(self):
        sorted_row = np.sort(self.matrix[-1, :])
        if self.m % 2 == 0:
            return (sorted_row[self.m // 2] + sorted_row[self.m // 2 - 1]) / 2
        else:
            return sorted_row[self.m // 2]
               
def task5():
    n = correct_input.validate_positive_int("Введите количество строк в матрице: ")
    m = correct_input.validate_positive_int("Введите количество столбцов в матрице: ")
    arr1 = MatrixStatistics(n, m)    
    arr1.create_matrix()
    print(arr1)
    #arr1 = arr1 + 2
    print()
    print(f"Cреднего значения всех элементов матрицы: {arr1.mean()}")
    print(f"Медиана матрицы: {arr1.median()}")
    print(f"Коэффициент корреляции между элементами матрицы:\n{arr1.corrcoef()}")
    print(f"Дисперсии всех элементов матрицы {arr1.var()}")
    print(f"Стандартного отклонения всех элементов матрицы: {arr1.std()}")
    print()
    #arr1 = arr1.sqrt()
    print(f"Медиана последней строки матрицы (программированием формулы): {arr1.individual_median_last_row()}")
    print(f"Медиана последней строки матрицы: {arr1.median_last_row()}")
    arr1.sort_last_row()
    print(arr1)
    #print(arr1[0][1])