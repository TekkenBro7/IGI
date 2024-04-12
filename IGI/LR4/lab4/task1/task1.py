"""
Выполнил: Снежко Максим Андреевич, группа 253505
Вариант 20
Задание 4
Исходные данные представляют собой словарь. Необходимо поместить их в файл, используя сериализатор. 
Организовать считывание данных, поиск, сортировку в соответствии с индивидуальным заданием. Обязательно использовать классы. 
Реализуйте два варианта: 1)формат файлов CSV; 2)модуль pickle
Реализуйте данные на учеников (фамилия, улица, дом, квартира). Составьте программу, определяющую, сколько учеников живет 
на улице, введенной с клавиатуры, списки учеников, живущих в доме с номером, введенном с клавиатуры.
"""
import csv
import pickle
from correct_input import validate_positive_int

class Student:
    def __init__(self, last_name, street, house, apartment):
        self.last_name = last_name
        self.street = street
        self.house = house
        self.apartment = apartment
     
    def __str__(self):
        return f"{self.last_name}, {self.street}, {self.house}, {self.apartment}"
    
    def to_dict(self):
        """Метод для того, чтобы преобразовать данные объекта в словарь"""
        return {
            'last_name': self.last_name,
            'street': self.street,
            'house': self.house,
            'apartment': self.apartment
        }    
 
class Database:
    filename_csv = "task1/student.csv" 
    filename_pickle = "task1/student.pickle"
    def __init__(self):
        self.data = []
    
    def save_to_csv(self):
        """Метод для того, чтобы записать данные в csv файл"""
        with open(self.filename_csv, 'w', encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(['Last Name', 'Street ', 'House', 'Apartment'])
            for student in self.data:
                writer.writerow([student['last_name'], student['street'], student['house'], student['apartment']])
    
    def load_from_csv(self):
        """Метод для того, чтобы считать данные с csv файла"""
        self.data = []
        with open(self.filename_csv, "r", encoding="utf-8", newline="") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                last_name, street, house, apartment = row
                student = {'last_name': last_name, 'street': street, 'house': house, 'apartment': apartment}
                self.data.append(student)     

    def save_to_pickle(self):
        """Метод для того, чтобы сохранить данные в pickle файл"""
        with open(self.filename_pickle, 'wb') as file:
            pickle.dump(self.data, file)
            
    def load_from_pickle(self):
        """Метод для того, чтобы загрузить данные с pickle файла"""
        with open(self.filename_pickle, 'rb') as file:
            self.data = pickle.load(file) 
 
class StudentDatabase(Database):
    def __init__(self):
        super().__init__()
        
    def __str__(self):
        return '\n'.join(str(student) for student in self.data)

    def add_student(self, student):
        """Метод для того, чтобы добавить студента в базу"""
        self.data.append(student)
 
    def get_count_students_by_street(self, street):
        """Метод для того, чтобы определить сколько студентов живут на конкретной улице, 
        введенным пользователем"""
        return len([student for student in self.data if student['street'] == street])
    
    def get_count_student_by_house(self, home):
        """Метод для того, чтобы определить, сколько студентов живут в конкретном доме,
        введенным пользователем"""
        return len([student for student in self.data if student['house'] == home])

    def sorting(self):
        self.data = sorted(self.data, key=lambda x: x['last_name'])
        
def task1():
    students = StudentDatabase() 
    student1 = Student('Ivanov', 'Lenin Street', '1', '12')
    student2 = Student('Aetrov', 'Gagarin Street', '2', '5')
    student3 = Student('Sidorov', 'Lenin Street', '2', '3')
    students.add_student(student1.to_dict())
    students.add_student(student2.to_dict())
    students.add_student(student3.to_dict())
    print(students)
    while True:
        last_name = input("Введите фамилию студента (или введите 'q' для завершения): ")
        if last_name == 'q':
            break
        street = input("Введите улицу проживания студента: ")
        house = input("Введите номер дома студента: ")
        apartment = validate_positive_int("Введите номер квартиры студента: ")
        student = Student(last_name, street, house, apartment)
        students.add_student(student.to_dict())
    print(students)

    students.sorting()
    print(students)
    
    students.save_to_csv()
    students.load_from_csv()
    students.save_to_pickle()
    students.load_from_pickle()

    street = input("Введите улицу для поиска количества студентов, проживающих там: ")
    print(f"Количество студентов проживающих на этой улице: {students.get_count_students_by_street(street)}")
    house = input("Введите номер дома для поиска количества студентов, проживающих там: ")
    print(f"Количество студентов проживающих в этом доме: {students.get_count_student_by_house(house)}")
    print(students)