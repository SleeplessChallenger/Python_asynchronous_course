from quart import Blueprint, Response

home = Blueprint('home', __name__)


@home.route('/')
def index():
	return  "Welcome to the city_scape API. " \
            "Use /api/sun/[zipcode]/[country code (e.g. us)] and" \
            "/api/weather/[zipcode]/[country code (e.g. us)] for API calls."

@home.errorhandler(404)
def not_found(_):
	return Response('The page was not found', status=404)
