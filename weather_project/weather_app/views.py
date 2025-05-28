import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CityForm
from .models import SearchHistory
from django.http import JsonResponse
from django.db.models import Count
import openmeteo_requests
from openmeteo_sdk.Variable import Variable
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_weather_data(city_name):
    """Получает данные о погоде из API."""
    try:
        # Прямое геокодирование для получения координат
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"

        # Конфигурируем сессию requests
        session = requests.Session()

        # Устанавливаем стратегию повторных попыток
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504],
                        allowed_methods=frozenset(['GET', 'POST']))

        # Связываем стратегию с сессией requests
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        geo_response = requests.get(geo_url, verify=False)
        geo_response.raise_for_status()  # Проверка на ошибки HTTP
        geo_data = geo_response.json()

        if not geo_data['results']:
            return None  # Город не найден

        latitude = geo_data['results'][0]['latitude']
        longitude = geo_data['results'][0]['longitude']

        # Запрос к API погоды
        om = openmeteo_requests.Client()
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'hourly': ['temperature_2m', 'relativehumidity_2m', 'windspeed_10m'],
            "current": ["temperature_2m", "relative_humidity_2m", 'windspeed_10m']
        }
        weather_responses = om.weather_api("https://api.open-meteo.com/v1/forecast", params=params)
        weather_response = weather_responses[0]
        current = weather_response.Current()
        current_windspeed_10m = current.Variables(2)
        current_variables = list(map(lambda i: current.Variables(i), range(0, current.VariablesLength())))
        current_temperature_2m = next(filter(lambda x: x.Variable() == Variable.temperature and x.Altitude() == 2, current_variables))
        current_relative_humidity_2m = next(filter(lambda x: x.Variable() == Variable.relative_humidity and x.Altitude() == 2, current_variables))
        weather_response = {
            'temperature_2m': round(current_temperature_2m.Value(), 2),
            'relativehumidity_2m': round(current_relative_humidity_2m.Value(), 2),
            'windspeed_10m': round(current_windspeed_10m.Value(), 2)
        }
        return weather_response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Ошибка при обработке данных: {e}")
        return None


def index(request):
    """Главная страница."""
    form = CityForm()
    weather_data = None

    def last_search():
        if request.user.is_authenticated:  # только для зарегистрированных
            last_search = SearchHistory.objects.filter(user=request.user).order_by('-timestamp').first()
            if last_search:
                last_city = last_search.city
                return last_city

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = request.POST.get('city')
            print(city)
            weather_data = get_weather_data(city)
            if request.user.is_authenticated:
                SearchHistory.objects.create(user=request.user, city=city)
            else:
                SearchHistory.objects.create(user=None, city=city) # анонимный пользователь
            last_city = last_search() or None
            return render(request, 'weather_app/index.html', {'form': form, 'weather_data': weather_data, 'last_city': last_city})
        else:
            form.add_error('city', "City not found.") # Добавляем ошибку в форму
    last_city = last_search() or None
    return render(request, 'weather_app/index.html', {'form': form, 'weather_data': weather_data, 'last_city': last_city})


@login_required
def history(request):
    """Отображает историю поиска для текущего пользователя."""
    history = SearchHistory.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'weather_app/history.html', {'history': history})


def search_stats(request):
    """API для статистики поисковых запросов."""
    city_counts = SearchHistory.objects.values('city').annotate(count=Count('city')).order_by('-count')
    data = [{'city': item['city'], 'count': item['count']} for item in city_counts]
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})