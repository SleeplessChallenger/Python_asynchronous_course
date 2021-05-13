from quart import abort, Blueprint, jsonify
from services import weather_service, sun_service, location_service

city = Blueprint('city', __name__)


@city.route('/api/weather/<zip_code>/<country>', methods=['GET'])
async def weather(zip_code: str, country: str):
	weather_data = await weather_service.get_current(zip_code, country)
	if not weather_data:
		abort(404)
	return jsonify(weather_data)

@city.route('/api/sun/<zip_code>/<country>', methods=['GET'])
async def sun(zip_code: str, country: str):
	lat, long = await location_service.get_lat_long(zip_code, country)
	sun_data = await sun_service.for_today(lat, long)
	if not sun_data:
		abort(404)
	return jsonify(sun_data)
