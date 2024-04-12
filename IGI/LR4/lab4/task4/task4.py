"""
Выполнил: Снежко Максим Андреевич, группа 253505
Вариант 20
Задание 4
Разработать базовые классы и классы наследники.
Программа должна содержать следующие базовые функции:
1) ввод значений параметров пользователем;
2) проверка корректности вводимых данных;
3) построение, закрашивание фигуры в выбранный цвет, введенный с клавиатуры, и подпись фигуры текстом, введенным с клавиатуры;
4) вывод фигуры на экран и в файл.
Вариант задания: построить параллелограмм по сторонам a, b и углу между ними A(в градусах).
"""
from abc import ABC, abstractmethod
import math
import correct_input
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

class GeometricFigure(ABC):
    @abstractmethod
    def calculate_area(self):
        """
        Абстрактный метод для вычисления площади геометрической фигуры.
        """
        pass
    
class Color:
    def __init__(self, color):
        self.color = color
        
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
        
class Parallelogram(GeometricFigure):
    filename_save_fig = "task4/parallelogram.png"
    """
    Класс, представляющий параллелограмм.
    """
    figure_type = "Параллелограмм"
    
    def __init__(self, a, b, text, angle, color):
        """
        Инициализация экземпляра параллелограмма.
        """
        self.a = a
        self.b = b
        self.text = text
        self.angle = math.radians(angle)
        self.color = Color(color)

    def __str__(self):
        return f"{Parallelogram.figure_type} - фигура задания, подпись фигуры: {self.text}"

    def calculate_area(self):
        """
        Вычисляет площадь параллелограмма.
        """
        return self.a * self.b * math.sin(self.angle)
    
    def get_info(self):
        """
        Возвращает информацию о параллелограмме.
        """
        return "{} - сторона a: {}, сторона b: {}, угол между а и b: {} градусов, цвет: {}, площадь: {}".format(
           self.figure_type, self.a, self.b, round(math.degrees(self.angle), 2), self.color.color, round(self.calculate_area(), 2))
    
    def draw(self):
        """
        Рисует параллелограмм.
        Создает графическое представление параллелограмма и сохраняет его в файл.
        """
        # Cоздает объект фигуры (fig) и набор подграфиков (ax)
        fig, ax = plt.subplots()
        vertices = np.array([[0, 0], [self.a, 0], [self.a + self.b * math.cos((self.angle)), self.b * math.sin((self.angle))], [self.b * np.cos((self.angle)), self.b * np.sin((self.angle))]])
        # Создание полигона на основе вершин
        parallelogram = plt.Polygon(vertices, closed=True, edgecolor='black', facecolor=self.color.color)
        # Добавление полигона на график
        ax.add_patch(parallelogram)
        # Настройка осей и масштаба
        ax.set_xlim(-10, max(self.a + self.b * math.cos(self.angle) + 1, self.a + 1))
        ax.set_ylim(-5, max(self.b * math.sin(self.angle) + 1, self.b + 1))
        # Добавление подписей осей
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        # Добавление заголовка графика
        ax.set_title('Параллелограм')
        ax.text(0.7 * self.a, 0.4 * self.b, self.text, ha='center', va='center')
        fig.savefig(self.filename_save_fig)
        plt.show()
    
def task4():
    a = correct_input.validate_positive_float("Введите длину стороны a параллелограмма: ")
    b = correct_input.validate_positive_float("Введите длину стороны b параллелограмма: ")
    A = correct_input.validate_angle("Введите угол между a и b: ")
    text = input("Введите подпись фигуры: ")
    color = correct_input.input_existing_color("Введите цвет параллелограмма: ")
    parallelogram = Parallelogram(a, b, text, A, color)
    print(parallelogram.get_info())
    print(parallelogram)
    parallelogram.draw()