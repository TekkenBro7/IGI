"""
Выполнил: Снежко Максим Андреевич, группа 253505
Вариант 20
Задание 4
В соответствии с заданием своего варианта доработать программу из ЛР3, использовав класс и обеспечить:
а) определение дополнительных параметров среднее арифметическое элементов последовательности, медиана, мода, дисперсия, СКО последовательности;
б) с помощью библиотеки matplotlib нарисовать графики разных цветов в одной координатной оси:
– график по полученным данным разложения функции в ряд, представленным в таблице,
– график соответствующей функции, представленной с помощью модуля math. Обеспечить отображение координатных осей, легенды, текста и аннотации.
Cохранить графики в файл
Степенное разложение: 1 / x = sum(0, +inf)x^n = 1 + x + x^2 + ..., |x|<1
"""
from tabulate import tabulate
import statistics
import numpy as np
import matplotlib.pyplot as plt
import math

class FunctionDecomposition():
    def __init__(self):
        self.x, self.epsilon = self.get_input_values()
        self.results = []
        self.values = []
    
    def __str__(self):
        return f"Значение x: {self.x}, значение epsilon: {self.epsilon}, последовательность разложения: {self.values}"
    
    @property
    def xValue(self):
        return self.x
    
    @xValue.setter
    def xValue(self, x):
        self.x = x
    
    @property
    def epsilonValue(self):
        return self.epsilon
    
    @epsilonValue.setter
    def epsilonValue(self, epsilon):
        self.epsilon = epsilon
        
    def get_input_values(self):
        """
        Получает значения аргумента x и точности epsilon от пользователя.
        Проверяет их на правильность ввода и возвращает их.
        Если значение аргумента x находится за пределами допустимого интервала (-1 < x < 1), 
        функция выводит сообщение об ошибке и требует повторный ввод данных.
        Если значение точности epsilon отрицательное, функция также выводит сообщение об ошибке и требует повторный ввод данных.
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
        
    def calculate_function(self, x = 1):
        """
        Выполняет разложение функции в степенной ряд для заданных значения аргумента x и точности epsilon.
        Заполняет списки x_values, series_values и math_values значениями аргумента, значениями разложения функции
        и значениями функции, вычисленными с помощью модуля math соответственно.
        
        Цикл выполяется, пока на какой-то итерации значении переменной degree будет меньше значения epsilon либо когда не 
        будет достигнуто 500 итераций
        """
        result, n = 0, 0
        self.results = []   
        math_result = 1 / (1 - self.x)
        if x != 1:
            self.x = x
        while True:
            degree = self.x ** n
            a = (self.x*self.x)**0.5**n
            n += 1
            if abs(degree) < self.epsilon or n > 499:
                break            
            result += degree
            self.results.append(result)
            self.values.append(degree)
        data = [[self.x, n, result, math_result, self.epsilon]]
        headers = ["x", "n", "F(x)", "Math F(x)", "eps"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
            
    def print_sequence(self):
        print(self.values) 
            
class AnalyzeFunc(FunctionDecomposition):
    file_decompose = "task3/sequence_fun.png"
    file_main_fun = "task3/main_fun.png"
    def __init__(self):
        super().__init__()
                               
    def avarage_sequence(self):
        if len(self.values) == 0:
            return None   
        return sum(self.values) / len(self.values)
    
    def median_sequence(self):
        if len(self.values) == 0:
            return None
        return statistics.median(self.values)
        
    def mode_sequence(self):
        if len(self.values) == 0:
            return None
        return statistics.mode(self.values)
      
    def variance_sequence(self):
        if len(self.values) == 0:
            return None
        return statistics.variance(self.values)
    
    def calculate_standard_deviation(self):
        if len(self.values) == 0:
            return None
        return statistics.stdev(self.values)
    
    def draw_fun(self):
        x = np.linspace(-10, 10, 250)
        y = 1 / (1 - x)        
        # Ищем индекс, ближайший к точке разрыва
        idx = np.abs(x - 1).argmin()
        # Добавляем значение NaN для y в точке разрыва
        y[idx] = np.nan
        # Создаем график
        plt.plot(x, y, color='black', linewidth=2)
        plt.ylim(-10,10)
        plt.legend(['График функции'])
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('График функции 1 / (1 - x)')
        # Добавляем аннотацию
        plt.annotate("Разрыв функции в точке x = 1" , xy=(1, 0), xytext=(-3, 5), color="blue",
             arrowprops=dict(facecolor="blue", shrink=0.01))
        # Добавляем сетку
        plt.grid(True)
        plt.savefig(self.file_main_fun)
        plt.show()
    
    def draw_sequence(self):
        if (self.x < 0):
            self.calculate_function(math.fabs(self.x))
            plt.plot(self.results, range(len(self.results)))
        else:   
            plt.plot(range(1, len(self.results) + 1), self.results)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('График последовательности разложения')
        plt.grid(True)
        plt.savefig(self.file_decompose)
        plt.show()
     
def task3():
    func = AnalyzeFunc()
    func.calculate_function()
    func.draw_sequence()
    func.draw_fun()
    func.print_sequence()
    print(f"Среднее арифметическое элементов последовательности: {func.avarage_sequence()}")
    print(f"Медиана последовательности: {func.median_sequence()}")
    print(f"Мода последовательности: {func.mode_sequence()}")
    print(f"Дисперсия последовательности: {func.variance_sequence()}")
    print(f"СКО последовательности: {func.calculate_standard_deviation()}")