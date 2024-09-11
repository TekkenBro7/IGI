import requests
from django.shortcuts import render


def nationalize(request):
    name = request.GET.get('name')  # Получаем имя из параметров запроса
    if name:
        url = f"https://api.nationalize.io/?name={name}"
        response = requests.get(url)
        data = response.json()
        return render(request, 'users/nationality.html', {'name': name, 'data': data})
    else:
        return render(request, 'users/nationality.html')