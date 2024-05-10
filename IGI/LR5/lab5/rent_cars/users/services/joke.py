import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from translate import Translator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class JokeService:
    @staticmethod
    def get_random_joke():
        return requests.get('https://official-joke-api.appspot.com/random_joke').json()



class JokeView(APIView):
    def get(self, request, format=None):
     #   return Response(JokeService.get_random_joke())
        joke = JokeService.get_random_joke()
        setup = joke['setup']
        punchline = joke['punchline']
        
        translator = Translator(from_lang="en", to_lang="ru")
        full_text = setup + " " + punchline
        full_text = translator.translate(full_text)
        
        translated_setup = translator.translate(setup)
        translated_punchline = translator.translate(punchline)
        
        return render(request, 'users/joke.html', {'full_text': full_text, 'joke': joke})
    
    
@login_required
def nationalize(request):
    name = request.GET.get('name')  # Получаем имя из параметров запроса
    if name:
        url = f"https://api.nationalize.io/?name={name}"
        response = requests.get(url)
        data = response.json()
        return render(request, 'users/nationality.html', {'name': name, 'data': data})
    else:
        return render(request, 'users/nationality.html')