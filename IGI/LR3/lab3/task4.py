"""
Выполнил: Снежко Максим, группа 253505
Вариант 20
Задание 4
а) определить количество слов, заключенных в кавычки;
б) определить, сколько раз повторяется каждая буква;
в) вывести в алфавитном порядке все словосочетания, отделенные запятыми 
02.03.2024
"""
def count_quoted_words(text):
    """
    Определяет количество слов, заключенных в кавычки. Как ' ', так и " "
    Функция count_quoted_words(text) подсчитывает количество слов, заключенных в кавычки (как в одинарных, так и в двойных),
    в заданном тексте text. Она итерирует по каждому символу в тексте и проверяет, находится ли функция внутри кавычек или 
    не внутри. Если функция находится внутри кавычек, она собирает символы для формирования слова. Когда функция выходит 
    из кавычек, она увеличивает счетчик слов. В конце выполнения функция выводит количество найденных слов на экран.
    """
    in_quotes = False
    word_count = 0
    current_word = ""
    for char in text:
        if char == "'" or char == '"':
            if in_quotes:
                in_quotes = False
                if current_word:
                    word_count += 1
                current_word = ""
            else:
                in_quotes = True
        elif (char.isalpha() or char == "'" or char == '"') and in_quotes:
            current_word += char
        elif char.isspace():
            if in_quotes and current_word:
                word_count += 1
            current_word = ""
    print("Количество слов, заключенных в кавычки:", word_count)

def count_each_letter(text):
    """ Определяет, сколько раз каждая буква встречается в тексте.
    Функция count_each_letter(text) подсчитывает, сколько раз каждая буква встречается в заданном тексте text. 
    Она создает словарь letters_count, где ключами являются буквы, а значениями - количество их вхождений в тексте. 
    Затем функция выводит полученный словарь на экран.
    """
    letters_count = {}
    for char in text.lower():
        if char.isalpha():
            letters_count[char] = letters_count.get(char, 0) + 1
    print("Количество каждой буквы в тексте:")
    print(letters_count)

def sort_phrases_between_comma(text):
    """ Выводит в алфавитном порядке все словосочетания, отделенные запятыми. """
    phrases = [phrase.strip() for phrase in text.split(',')]
    print("Словосочетания, разделенные запятыми в тексте и отсортированные в алфавитном порядке:")
    print(*sorted(phrases), sep='\n')

def task4():
    """ Основная функция программы для решения задачи 4. """
    text = "So shewas considering in her own mind, as well asshe could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."      
    count_quoted_words(text)
    count_each_letter(text)
    sort_phrases_between_comma(text)