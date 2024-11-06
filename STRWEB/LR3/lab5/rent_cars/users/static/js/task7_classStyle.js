class Person {
    constructor(lastName, firstName, middleName, age) {
        this.lastName = lastName;
        this.firstName = firstName;
        this.middleName = middleName;
        this.age = age;
    }
    get fullName() {
        return `${this.lastName} ${this.firstName} ${this.middleName}`;
    }
    get personAge() {
        return this.age;
    }
    set personAge(newAge) {
        if (newAge < 1 || newAge > 120) {
            throw new Error("Возраст должен быть в пределах от 1 до 120.");
        }
        this.age = newAge;
    }
    displayInfo() {
        return `ФИО: ${this.fullName}, Возраст: ${this.age}`;
    }
    static addPersonFromForm(event) {
        event.preventDefault();

        const lastName = document.getElementById("personLastName").value;
        const firstName = document.getElementById("personFirstName").value;
        const middleName = document.getElementById("personMiddleName").value;
        const age = parseInt(document.getElementById("personAge").value, 10);

        const newPerson = new Person(lastName, firstName, middleName, age);
        if (!Person.isPersonExists(newPerson)) {
            Person.people.push(newPerson);
            Person.displayPeople();
        } else {
            alert("Человек с таким ФИО уже существует в списке людей.");
        }
        //    Person.people.push(newPerson);
        //    Person.displayPeople();
    }
    static isPersonExists(person) {
        return Person.people.some(existingPerson => existingPerson.fullName === person.fullName);
    }
    static displayPeople() {
        const personListDiv = document.getElementById("personList");
        personListDiv.innerHTML = "";

        Person.people.forEach(person => {
            const personDiv = document.createElement("div");
            personDiv.textContent = person.displayInfo();
            personListDiv.appendChild(personDiv);
        });
    }
}

Person.people = [];

class Employee extends Person {
    constructor(lastName, firstName, middleName, age, experience) {
        super(lastName, firstName, middleName, age);
        this.experience = experience;
    }
    get workExperience() {
        return this.experience;
    }
    set workExperience(newExperience) {
        if (newExperience < 0 || newExperience > 100) {
            throw new Error("Стаж должен быть в пределах от 0 до 100.");
        }
        this.experience = newExperience;
    }
    static addEmployeeFromForm(event) {
        event.preventDefault();

        const lastName = document.getElementById("lastName").value;
        const firstName = document.getElementById("firstName").value;
        const middleName = document.getElementById("middleName").value;
        const age = parseInt(document.getElementById("age").value, 10);
        const experience = parseInt(document.getElementById("experience").value, 10);

        const newEmployee = new Employee(lastName, firstName, middleName, age, experience);
        if (!Employee.isEmployeeExists(newEmployee)) {
            Employee.employees.push(newEmployee);
            if (!Person.isPersonExists(newEmployee)) {
                Person.people.push(newEmployee);
                Person.displayPeople();
            }
            Employee.displayEmployees();
            Employee.displayYoungExperiencedEmployees();
        } else {
            alert("Сотрудник с таким ФИО уже существует в списке сотрудников.");
        }
        //   Employee.employees.push(newEmployee);
        //   Employee.displayEmployees();
        //   Employee.displayYoungExperiencedEmployees();
    }
    static isEmployeeExists(employee) {
        return Employee.employees.some(existingEmployee => existingEmployee.fullName === employee.fullName);
    }
    static displayEmployees() {
        const employeeListDiv = document.getElementById("employeeList");
        employeeListDiv.innerHTML = "";
        Employee.employees.forEach(employee => {
            const employeeDiv = document.createElement("div");
            employeeDiv.textContent = `${employee.fullName}, Возраст: ${employee.personAge}, Стаж: ${employee.workExperience} лет`;
            employeeListDiv.appendChild(employeeDiv);
        });
    }
    static displayYoungExperiencedEmployees() {
        const countInput = document.getElementById("employeeCount");
        const count = parseInt(countInput.value, 10) || 3;

        const youngEmployeesDiv = document.getElementById("youngEmployees");
        youngEmployeesDiv.innerHTML = "";
        const eligibleEmployees = Employee.employees.filter(emp => emp.workExperience >= 3);
        const youngExperiencedEmployees = eligibleEmployees
            .sort((a, b) => a.personAge - b.personAge)
            .slice(0, count);
        youngExperiencedEmployees.forEach(employee => {
            const employeeDiv = document.createElement("div");
            employeeDiv.textContent = `${employee.fullName}, Возраст: ${employee.personAge}, Стаж: ${employee.workExperience} лет`;
            youngEmployeesDiv.appendChild(employeeDiv);
        });
    }
}

Employee.employees = [];
document.getElementById("employeeForm").addEventListener("submit", Employee.addEmployeeFromForm);
document.getElementById("personForm").addEventListener("submit", Person.addPersonFromForm);