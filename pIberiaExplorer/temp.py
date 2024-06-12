import os 
import sys
import django

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to the Python path
if project_root not in sys.path:
    sys.path.append(project_root)

# Set the environment variable for the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pIberiaExplorer.settings')
django.setup()

# Rutas de los proyectos
path_proyecto = os.path.dirname(os.path.abspath(__file__))
path_proyecto_padre = os.path.dirname(path_proyecto)

from django.db import models
from appIberiaExplorer.models import Continente, Pais, Ciudad

continentes = [
    'Europa',
    'Asia',
    'África',
    'América',
    'Oceanía',
]

pais = ['España']

cities = [
    'Madrid',
    'Barcelona',
    'Valencia',
    'Seville',
    'Zaragoza',
    'Málaga',
    'Murcia',
    'Palma',
    'Las Palmas de Gran Canaria',
    'Bilbao',
    'Alicante',
    'Córdoba',
    'Valladolid',
    'Vigo',
    'Gijón',
    'L\'Hospitalet de Llobregat',
    'A Coruña',
    'Vitoria-Gasteiz',
    'Granada',
    'Elche'
]

for continent_name in continentes:
    continent = Continente(nombre=continent_name)
    continent.save()
    
for country_name in pais:
    country = Pais(nombre=country_name, continente=Continente.objects.get(nombre='Europa'))
    country.save()

for city_name in cities:
    city = Ciudad(nombre=city_name, pais=Pais.objects.get(nombre='España'))
    city.save()