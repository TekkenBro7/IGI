import re
import zipfile

class FileAnalyzer:
    filename_read = "task2/task2Test.txt"
    def __init__(self):
        self.text = self.read_text_from_file()

    def read_text_from_file(self):
        """Метод для того, чтобы считать текст с определенного файла"""
        try:
            with open(self.filename_read, "r", encoding="utf-8") as fileRead:
                return fileRead.read()
        except Exception as ex:
            print("Ошибка при чтении с файла: ", ex)
            return ""

class TextAnalyzer(FileAnalyzer):
    def __init__(self, writefilename):
        super().__init__()
        self.writefilename = writefilename
        self.initial_count = self.count_initials()
    
    def __str__(self):
        return f"Путь к файлу: {self.filename}, его содержание:\n {self.text}"
    
    @property
    def namefile(self):
        return self.filename_read
    
    @namefile.setter
    def namefile(self, name):
        self.filename_read = name
        self.text = self.read_text_from_file()
        self.initial_count = self.count_initials()
           
    def count_sentences(self):
        """Метод для того, чтобы  определить количество предложений в тексте"""
        sentence_count = len(re.findall(r"[.!?]", self.text)) + self.count_ellipsis()
        return sentence_count - self.initial_count
    
    def count_ellipsis(self):
        """Метод для того, чтобы определить количество многоточий в тексте"""
        ellipsis_count = len(re.findall(r"\.\.\.", self.text))
        return ellipsis_count
        
    def count_initials(self):
        """Метод для того, чтобы  определить инициалы в тексте"""
        initials = re.findall(r'\b[А-ЯA-Z]\.[А-ЯA-Z]\.[А-ЯA-Z]', self.text)
        initial_res = len(initials) * 2 if initials else 0
        return initial_res
    
    def count_sentences_each_type(self):
        """Метод для того, чтобы  определить, сколько повествовательных, вопросительных 
        и побудительных предложений в тексте"""
        narrative_count = len(re.findall(r"[.]", self.text)) + self.count_ellipsis() - self.initial_count
        questioin_count = len(re.findall(r"[?]", self.text))
        imperative_count = len(re.findall(r"[!]", self.text))
        return (narrative_count, questioin_count, imperative_count)
    
    def count_words(self):
        """Метод для того, чтобы определить количество слов в тексте"""
        words = re.findall(r'\b[И-Яа-яa-zA-Z]+\b', self.text)
        return len(words)

    def count_characters(self):
        """Метод для того, чтобы  определить количетсво символов в словах"""
        words = re.findall(r'\b\w+\b', self.text)
        total_chars = sum(len(char) for char in words)
        return total_chars
    
    def calculate_avg_sentence_length(self):
        """Метод для того, чтобы определить среднюю длину предложения в символах"""
        sentence_count = self.count_sentences()
        total_chars = self.count_characters()
        avg_sentence_length = total_chars / sentence_count if sentence_count != 0 else 0
        return avg_sentence_length

    def calculate_avg_word_length(self):
        """Метод для того, чтобы определить среднюю длину слова в тексте"""
        total_chars = self.count_characters()
        word_count = self.count_words()
        avg_word_length = total_chars / word_count if word_count != 0 else 0
        return avg_word_length

    def count_smileys(self):
        """Метод для того, чтобы определить количество смайликов в тексте"""
        smile_count = len(re.findall(r'([:;]-*([()\[\]])\2*)', self.text)) 
        return smile_count
    
    def find_dates(self):
        """Метод для того, чтобы  найти всех даты в формате '2007'"""
        date_pattern = r"\b(\d{4})\b" # r'\b\d{2}\.\d{2}\.\d{4}\b'
        dates = re.findall(date_pattern, self.text)
        return dates
    
    def find_words(self):
        """Метод для того, чтобы из текста получить список слов, у которых третья 
        с конца буква согласная, а предпоследняя - гласная"""
        words = re.findall(r'\b\w+[^ aeiouyаеёиоуыэюя][aeiouyаеёиоуыэюя][a-zа-я]\b', self.text)
        return words
        
    def longest_word_and_place(self):
        """Метод для того, чтобы определить самое длинное слово и его порядковый номер"""
        words = re.findall(r'\b[И-Яа-яa-zA-Z]+\b', self.text)
        longest_word = max(words, key=len)
        max_word_index = words.index(longest_word)
        return (longest_word, max_word_index)
    
    def each_odd_num(self):
        """Метод для того, чтобы определить каждое нечетное слово"""
        words = re.findall(r'\b[И-Яа-яa-zA-Z]+\b', self.text)
        odd_word = []
        for i, word in enumerate(words, 1):
            if i % 2 != 0:
                odd_word.append(word)
        return odd_word
    
    def print_info_about_file(self):
        """Метод для того, чтобы вывести на экран всю информацию о файле"""
        print(f"\nКоличество предложений в тексте: {self.count_sentences()}")
        print(f"Количество повествовательных предложений в тексте: {self.count_sentences_each_type()[0]}")
        print(f"Количество вопросительных предложений в тексте: {self.count_sentences_each_type()[1]}")
        print(f"Количество побудительных предложений в тексте: {self.count_sentences_each_type()[2]}")
        print(f"Средняя длина предложения в символах: {self.calculate_avg_sentence_length()}")
        print(f"Средняя длина слова в тексте в символах: {self.calculate_avg_word_length()}")
        print(f"Количество смайликов в тексте: {self.count_smileys()}")
        print(f"Список дат: {self.find_dates()}")
        print(f"Третья с конца буква согласная, предпоследняя гласная: {self.find_words()}")
        print(f"Количество слов в файле: {self.count_words()}")
        print(f"Самое длинное слово в файле:'{self.longest_word_and_place()[0]}', его позиция: {self.longest_word_and_place()[1]}")
        print(f"Нечетные слова в файле: {self.each_odd_num()}")     

class ExtendedTextAnalyzer(TextAnalyzer):
    def __init__(self, writefilename):
        super().__init__(writefilename)
        
    def write_results(self):
        """Метод для того, чтобы записать всю информацию в новый файл"""
        try:
            with open(self.writefilename, "w", encoding="utf-8") as file:
                file.write(f"Количество предложений в тексте: {self.count_sentences()}\n")
                file.write(f"Количество повествовательных предложений в тексте: {self.count_sentences_each_type()[0]}\n")
                file.write(f"Количество вопросительных предложений в тексте: {self.count_sentences_each_type()[1]}\n")
                file.write(f"Количество побудительных предложений в тексте: {self.count_sentences_each_type()[2]}\n")
                file.write(f"Средняя длина предложения в символах: {self.calculate_avg_sentence_length()}\n")
                file.write(f"Средняя длина слова в тексте в символах: {self.calculate_avg_word_length()}\n")
                file.write(f"Количество смайликов в тексте: {self.count_smileys()}\n")
                file.write(f"Список дат: {self.find_dates()}\n")
                file.write(f"Третья с конца буква согласная, предпоследняя гласная: {self.find_words()}\n")
                file.write(f"Количество слов в файле: {self.count_words()}\n")
                file.write(f"Самое длинное слово в файле:'{self.longest_word_and_place()[0]}', его позиция: {self.longest_word_and_place()[1]}\n")
                file.write(f"Нечетные слова в файле: {self.each_odd_num()}")                
        except Exception as ex:
            print("Ошибка при записи результатов в файл:", ex)

    def write_to_zip(self):
        """Метод для того, чтобы записать файлы в zip"""
        try:
            with zipfile.ZipFile(self.writefilename + ".zip", "w") as zip:
                zip.write(self.filename_read)
                zip.write(self.writefilename)
        except Exception as ex:
            print("Ошибка при архировании файла:", ex)
    
    def print_info_about_zip(self):
        """Метод для того, чтобы получить информацию о zip-файле"""
        try:
            with zipfile.ZipFile(self.writefilename + ".zip", "r") as zip:
                file_info = zip.getinfo(self.filename_read)
                print("Информация о файле в архиве:")
                print(f"Имя файла: {file_info.filename}")
                print(f"Размер файла (байты): {file_info.file_size}")
                print(f"Время создания файла: {file_info.date_time}")
        except Exception as ex:
            print("Ошибка при архировании файла:", ex)                              
                        
def task2(writeFileName):
    analyzer = ExtendedTextAnalyzer(writeFileName)
    analyzer.write_results()
    analyzer.print_info_about_file()
    analyzer.write_to_zip()
    analyzer.print_info_about_zip()