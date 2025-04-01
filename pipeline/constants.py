# isolate variables into an env file or something similar
CITIES_TO_MONITOR = {
    'Ljubljana,Slovenia': '',
    'Zagreb,Croatia': '',
    'Vienna,Austria': '',
    'Budapest,Hungary': '',
    'Milano,Italy': '',
    'Miami,Florida,US': '',
}
CITY_URL = 'https://api.openweathermap.org/geo/1.0/direct'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather'

OW_KEY = 'f2b5d36fc1f975ace88d6ac18f0d6f42'
COORD_PARAMETERS = {
    'limit': '3',
    'q': '',
    'appid': OW_KEY,
}
WEATHER_PARAMETERS = {
    'lat': '',
    'lon': '',
    'appid': OW_KEY,
}
HEADERS = {
    'Accepts': 'application/json',
}
TABLE_COLUMN_MAP = {
    'coord_lon': 'location_longitude',
    'coord_lat': 'location_latitude',
    'weather[0]_main': 'weather',
    'weather[0]_description': 'weather_description',
    'main_temp': 'temperature',
    'main_feels_like': 'feels_like',
    'main_temp_min': 'minimum_temperature',
    'main_temp_max': 'maximum_temperature',
    'main_pressure': 'pressure',
    'main_humidity': 'humidity',
    'main_sea_level': 'sea_level_pressure',
    'main_grnd_level': 'ground_level_pressure',
    'visibility': 'visibility',
    'wind_speed': 'wind_speed',
    'wind_deg': 'wind_direction_degrees',
    'rain_1h': 'rain_precipitation',
    'snow_1h': 'snow_precipitation',
    'clouds_all': 'cloudiness_pct',
    'dt': 'datetime',
    'sys_country': 'country',
    'sys_sunrise': 'sunrise',
    'sys_sunset': 'sunset',
    'timezone': 'timezone',
    'id': 'city_id',
    'name': 'city_name',
}
API_METRICS_COLUMNS = ['call_dt', 'status_code', 'safe_url', 'elapsed', 'content_length']
