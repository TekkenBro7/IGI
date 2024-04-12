import pandas as pd
from IPython.display import display
import re

def convert_to_minutes(time_string):
    hours = 0
    minutes = 0
    # Поиск числовых значений для часов и минут
    hours_match = re.search(r'(\d+)h', time_string)
    minutes_match = re.search(r'(\d+)min', time_string)
    # Преобразование значения часов в минуты
    if hours_match:
        hours = int(hours_match.group(1))
    # Преобразование значения минут в минуты
    if minutes_match:
        minutes = int(minutes_match.group(1))
    total_minutes = hours * 60 + minutes
    return total_minutes

def task6():
     data = [10, 20, 30, 40, 50]
     series = pd.Series(data)
     print(series)
     index = ['a', 'b', 'c', 'd', 'e']
     series2 = pd.Series(data, index=index)
     print(series2)
     print(series2[['a', 'b']])
     display(series2)
     # Доступ к элементу по значению индекса
     print(series2.loc['a'])
     # Доступ к элементу по числовому индексу
     print(series2.iloc[2])
     df = pd.DataFrame({
          'country': ['Kazakhstan', 'Russia', 'Belarus', 'Ukraine'],
          'population': [17.04, 143.5, 9.5, 45.5],
          'square': [2724902, 17125191, 207600, 603628]
     }, index=['KZ','RU','BY','UA'])
     print(df)
     print(df['country'])
     print(df[df.population > 10][['country', 'square']])
     print(df.reset_index())

     dataFrame = pd.read_csv('task6/Action.csv', sep=',')
     print("Первые пять строк:")
     print(dataFrame.head()) 
     print("Последние пять строк:")
     print(dataFrame.tail())
     print("Информация о данных:")
     print(dataFrame.info())
     print("Основные статистические характеристики:")
     print(dataFrame.describe())
     # Средний рейтинг фильмов
     average_rating = round(dataFrame["rating"].mean(), 2)
     print("Средний рейтинг фильмов:", average_rating)
     # Преобразуем столбец "run_length" в числовое значение продолжительности в минутах
     dataFrame["run_length"] = dataFrame["run_length"].apply(convert_to_minutes)
     # Вычисляем среднюю продолжительность фильмов
     average_run_length = dataFrame["run_length"].mean()
     # Выбираем фильмы с продолжительностью ниже среднего
     short_movies = dataFrame[dataFrame["run_length"] < average_run_length]
     # Вычисляем средний рейтинг фильмов с продолжительностью ниже среднего
     average_rating = round(short_movies["rating"].mean())

     # Вычисление среднего рейтинга для фильмов с максимальной продолжительностью
     max_run_length = dataFrame['run_length'].max()
     avg_rating_max_run_length = dataFrame[dataFrame['run_length'] == max_run_length]['rating'].mean()
     print(f"Максимальная длительность: {max_run_length} минут, средний рейтинг максимального по продолжительности фильма: {avg_rating_max_run_length}")

     # Вычисление среднего рейтинга для фильмов с минимальной продолжительностью
     min_run_length = dataFrame['run_length'].min()
     avg_rating_min_run_length = dataFrame[dataFrame['run_length'] == min_run_length]['rating'].mean()
     print(f"Минимальная длительность: {min_run_length} минут, средний рейтинг минимального по продолжительности фильма: {avg_rating_min_run_length}")

     # Вычисление отношения средних рейтингов
     ratio = avg_rating_max_run_length / avg_rating_min_run_length
     print("Отношение средних рейтингов (максимальная продолжительность / минимальная продолжительность):", ratio)

     max_reviews = dataFrame["num_reviews"].max()
     movie_with_max_reviews = dataFrame[dataFrame["num_reviews"] == max_reviews]["name"].values[0]
     print("Фильм с наибольшим количеством отзывов:", movie_with_max_reviews)
     print("Количество отзывов:", max_reviews)

     threshold_rating = 8
     average_reviews_above_threshold = dataFrame[dataFrame["rating"] > threshold_rating]["num_reviews"].mean()
     print(f"Среднее количество отзывов для фильмов с рейтингом выше {threshold_rating}: {round(average_reviews_above_threshold, 2)}")