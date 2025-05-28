from django.test import TestCase, Client
from django.urls import reverse
from .models import SearchHistory
from django.contrib.auth.models import User
import json

class WeatherAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.city = SearchHistory.objects.create(user=self.user, city='Чебоксары')

    def test_history_view(self):
        self.client.login(username='testuser', password='testpassword')
        SearchHistory.objects.create(user=self.user, city=self.city)
        response = self.client.get(reverse('history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'weather_app/history.html')
        self.assertEqual(len(response.context['history']), 2)

    def test_search_stats_api(self):
        self.client.login(username='testuser', password='testpassword')
        SearchHistory.objects.create(user=self.user, city=self.city)
        response = self.client.get(reverse('search_stats'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['city'], 'Чебоксары')
        self.assertEqual(data[0]['count'], 1)

