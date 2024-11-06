let sortDirection = {};
let currentPage = 1;
let rows;
let table;
let tbody;
let mainRows;
const rowsPerPage = 3;


document.addEventListener('DOMContentLoaded', function() {
    table = document.getElementById("employee-table");
    tbody = table.querySelector("tbody");
    rows = Array.from(tbody.querySelectorAll("tr"));
    mainRows = rows;


    displayPage(currentPage);
});

function displayPage(page) {
    tbody.classList.add("fade-out");
    setTimeout(() => {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;
        tbody.innerHTML = '';
        rows.slice(start, end).forEach(row => tbody.appendChild(row));
        updatePagination(rows.length, page);
        tbody.classList.remove("fade-out");
        tbody.classList.add("fade-in");
        setTimeout(() => {
            tbody.classList.remove("fade-in");
        }, 500);
    }, 500);
}


function applyFilter() {
    rows = mainRows;
    const filterText = document.getElementById("filter-input").value.toLowerCase();
    filteredRows = rows.filter(row => {
        return Array.from(row.cells).some(cell =>
            cell.innerText.toLowerCase().includes(filterText)
        );
    });
    currentPage = 1;
    filteredRows.forEach(row => tbody.appendChild(row));
    rows = filteredRows;
    displayPage(currentPage);
    deleteSortIcons();
}

function sortTable(columnIndex) {
    sortDirection[columnIndex] = sortDirection[columnIndex] === 'asc' ? 'desc' : 'asc';
    rows.sort((rowA, rowB) => {
        const cellA = rowA.cells[columnIndex].innerText.toLowerCase();
        const cellB = rowB.cells[columnIndex].innerText.toLowerCase();
        if (cellA < cellB) return sortDirection[columnIndex] === 'asc' ? -1 : 1;
        if (cellA > cellB) return sortDirection[columnIndex] === 'asc' ? 1 : -1;
        return 0;
    });
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
    displayPage(currentPage);
    updateSortIcons(columnIndex);
}

function updatePagination(totalRows, page) {
    const totalPages = Math.ceil(totalRows / rowsPerPage);
    const paginationControls = document.getElementById("pagination-controls");
    paginationControls.innerHTML = '';
    const prevButton = document.createElement('button');
    prevButton.innerHTML = '&#10094';
    prevButton.disabled = page === 1;
    prevButton.addEventListener('click', () => {
        if (page > 1) {
            currentPage--;
            displayPage(currentPage);
        }
    });
    paginationControls.appendChild(prevButton);
    const maxPagesToShow = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxPagesToShow / 2));
    let endPage = Math.min(totalPages, startPage + maxPagesToShow - 1);
    if (endPage - startPage + 1 < maxPagesToShow) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }
    for (let i = startPage; i <= endPage; i++) {
        const pageButton = document.createElement('button');
        pageButton.textContent = i;
        if (i === currentPage) {
            pageButton.disabled = true;
            pageButton.classList.add('active-page');
        }
        pageButton.addEventListener('click', () => {
            currentPage = i;
            displayPage(currentPage);
        });
        paginationControls.appendChild(pageButton);
    }
    const nextButton = document.createElement('button');
    nextButton.innerHTML = '&#10095';
    nextButton.disabled = page === totalPages;
    nextButton.addEventListener('click', () => {
        if (page < totalPages) {
            currentPage++;
            displayPage(currentPage);
        }
    });
    paginationControls.appendChild(nextButton);
}

function deleteSortIcons() {
    const headers = document.querySelectorAll("#employee-table th");
    headers.forEach((header, index) => {
        header.classList.remove("sort-asc", "sort-desc");
    });
}

function updateSortIcons(columnIndex) {
    const headers = document.querySelectorAll("#employee-table th");
    headers.forEach((header, index) => {
        header.classList.remove("sort-asc", "sort-desc");
        if (index === columnIndex) {
            header.classList.add(sortDirection[columnIndex] === 'asc' ? 'sort-asc' : 'sort-desc');
        }
    });
}

function showDetails(row) {
    const cells = row.cells;

    document.getElementById("detail-name").innerText = cells[0].innerText;
    document.getElementById("detail-photo").innerHTML = `<img src="${cells[1].querySelector('img').src}" alt="Фото" width="100">`; // Фото
    document.getElementById("detail-job").innerText = cells[2].innerText;
    document.getElementById("detail-phone").innerText = cells[3].innerText;
    document.getElementById("detail-email").innerText = cells[4].innerText;

    document.getElementById("details-block").style.display = "block";
}


function toggleAddEmployeeForm() {
    const form = document.getElementById("add-employee-form");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

function validateUrl(url) {
    const urlPattern = /^(https?:\/\/)([a-zA-Z0-9.-]+)\.(php|html)$/;
    return urlPattern.test(url);
}

function validateEmail(url) {
    const urlPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return urlPattern.test(url);
}

function validatePhone(phone) {
    const phonePattern = /^(8|\+?375)\s*(\(?\d{2,3}\)?)\s?\d{3}[\s-]?\d{2}[\s-]?\d{2}$/;
    return phonePattern.test(phone);
}

document.getElementById("id_url").addEventListener("blur", function() {
    const urlInput = document.getElementById("id_url");
    const urlError = document.getElementById("url-error");
    if (!validateUrl(urlInput.value)) {
        urlError.textContent = "Неверный формат URL. Должен начинаться с http:// или https:// и заканчиваться на .php или .html";
        urlError.style.display = "block";
        urlInput.style.borderColor = "red";
        urlInput.style.backgroundColor = "#ffe6e6";
    } else {
        urlError.style.display = "none";
        urlInput.style.borderColor = "";
        urlInput.style.backgroundColor = "";
    }
});

document.getElementById("id_phone_number").addEventListener("blur", function() {
    const phoneInput = document.getElementById("id_phone_number");
    const phoneError = document.getElementById("phone-error");
    if (!validatePhone(phoneInput.value)) {
        phoneError.textContent = "Неверный формат телефона. Пример: 80291112233, +375 (29) 111-22-33, 8 (029) 111 22 33";
        phoneError.style.display = "block";
        phoneInput.style.borderColor = "red";
        phoneInput.style.backgroundColor = "#ffe6e6";
    } else {
        phoneError.style.display = "none";
        phoneInput.style.borderColor = "";
        phoneInput.style.backgroundColor = "";
    }
});

document.getElementById("id_email").addEventListener("blur", function() {
    const emailInput = document.getElementById("id_email");
    const emailError = document.getElementById("email-error");
    if (!validateEmail(emailInput.value)) {
        emailError.textContent = "Неверная почта.";
        emailError.style.display = "block";
        emailInput.style.borderColor = "red";
        emailInput.style.backgroundColor = "#ffe6e6";
    } else {
        emailError.style.display = "none";
        emailInput.style.borderColor = "";
        emailInput.style.backgroundColor = "";
    }
});

function checkAllFieldsValid() {
    const name = document.getElementById("id_user").options[document.getElementById("id_user").selectedIndex].text;
    const photoEmp = document.getElementById("id_photo").value;
    const job_description = document.getElementById("id_job_description").value;
    const phone = document.getElementById("id_phone_number").value;
    const email = document.getElementById("id_email").value;
    const url = document.getElementById("id_url").value;

    if (validateUrl(url) && validatePhone(phone) && name && photoEmp && job_description && validateEmail(email)) {
        document.getElementById("subm_button").style.display = "block";
    }

}

document.getElementById("id_user").addEventListener("blur", checkAllFieldsValid);
document.getElementById("id_photo").addEventListener("blur", checkAllFieldsValid);
document.getElementById("id_job_description").addEventListener("blur", checkAllFieldsValid);
document.getElementById("id_phone_number").addEventListener("blur", checkAllFieldsValid);
document.getElementById("id_email").addEventListener("blur", checkAllFieldsValid);
document.getElementById("id_url").addEventListener("blur", checkAllFieldsValid);

function validateAndSubmit() {
    document.getElementById("employee-form").submit();
    document.getElementById("employee-form").reset();
    document.getElementById("subm_button").style.display = "none";
}

function generateBonusText() {
    const checkboxes = document.querySelectorAll(".employee-checkbox:checked");
    const selectedEmployees = Array.from(checkboxes).map(checkbox => checkbox.getAttribute("data-name"));
    document.getElementById("bonus-text").style.display = "block";
    if (selectedEmployees.length > 0) {
        const bonusText = `Сотрудники, которых премируют: ${selectedEmployees.join(", ")}.`;
        document.getElementById("bonus-text").textContent = bonusText;
    } else {
        document.getElementById("bonus-text").textContent = "Выберите сотрудников для премирования.";
    }
}