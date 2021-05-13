from quart import Quart
from views.city_api import city
from views.home import home
from config import settings
import services.weather_service
import services.sun_service
import services.location_service

app = Quart(__name__)
is_debug = True


app.register_blueprint(home)
app.register_blueprint(city)


def configure_app():
	mode = 'dev' if is_debug else 'prod'
	data = settings.load(mode)

	services.weather_service.global_init(data.get('weather_key'))
	services.sun_service.use_cached_data = data.get('use_cached_data')
	services.location_service.use_cached_data = data.get('use_cached_data')

	print(f"Using cached data? {data.get('use_cached_data')}")

def run_web_app():
	app.run(debug=is_debug, port=5001)


configure_app()


# if __name__ == '__main__':
# 	run_web_app()
