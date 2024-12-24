import json
import os
from django.core.management.base import BaseCommand
from user_profile.models import City

class Command(BaseCommand):
    help = 'Load city data into the City model'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.path.dirname(__file__), 'city_data.json')
        with open(file_path, 'r') as file:
            city_data = json.load(file)
            for city in city_data:
                City.objects.get_or_create(name=city['name'])
        self.stdout.write(self.style.SUCCESS('Successfully loaded city data'))
