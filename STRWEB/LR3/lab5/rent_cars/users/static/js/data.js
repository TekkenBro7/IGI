document.getElementById("vacancies-container").style.display = "none";

function checkAge() {
    let birthDateStr = prompt("Введите дату рождения (YYYY-MM-DD):", "2000-01-01");

    const datePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$/;
    if (!datePattern.test(birthDateStr)) {
        alert("Дата введена некорректно. Пожалуйста, обновите страницу и попробуйте снова.");
        return;
    }
    let birthDate = new Date(birthDateStr);
    if (isNaN(birthDate.getTime())) {
        alert("Дата введена некорректно. Пожалуйста, обновите страницу и попробуйте снова.");
        return;
    }
    let today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    if (age < 0) {
        alert("Дата введена больше текущей даты. Пожалуйста, обновите страницу и попробуйте снова.");
    }
    let monthDifference = today.getMonth() - birthDate.getMonth();
    if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    const days = [
        'Воскресенье',
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота'
    ];
    if (age < 18) {
        alert(`Вы несовершеннолетний. Вам необходимо разрешение родителей на использование этой страницы. Ваша дата рождения ${birthDate.toLocaleDateString()}, это - ${days[birthDate.getDay()]}`);
        return;
    }
    alert(`Вы совершеннолетний. Ваша дата рождения ${birthDate.toLocaleDateString()}, это - ${days[birthDate.getDay()]}`);
    document.getElementById("vacancies-container").style.display = "block";
    return true;
}

window.onload = checkAge();