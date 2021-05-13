**Web Frameworks based on asyncio**

Directory with files: `asyncio_based_web_frameworks`

<ins><i>Quart</i></ins> is a good alternative to Flask if you need asynchronous operations.<br>
Due to similarity of their API we can tweak them by changing everything with **flask to quart**

Next, look at following function:
It is an async view which waits for coroutines that are async themselves.<br>
Those coroutines implement aiohttp instead of requests and use asyncio for methods like sleep etc

```bash
@city.route('/api/sun/<zip_code>/<country>', methods=['GET'])
async def sun(zip_code: str, country: str):
	lat, long = await location_service.get_lat_long(zip_code, country)
	sun_data = await sun_service.for_today(lat, long)
	if not sun_data:
		abort(404)
	return jsonify(sun_data)
  ```

There is no direct difference in performance, but the thread that runs the web service is now free to take other request while it’s waiting.<br>
Previously that thread was blocked waiting for the response.

![Alt text](/ImageRepo/Libraries_first.png?raw=true)

![Alt text](/ImageRepo/Libraries_first.png?raw=true)

We can compare how `Flask` and `Quart` relate to each other by looking at the following two images

In Quart we need to **await async methods** which are implemented somewhere else. And this **await** is the key to performance boost. While we are waiting for get_lat_long & for_today, instead of just literally waiting as it’s in Flask, we can run other methods

<ins>Load testing the app</ins>

**Note:** when using external services, not local database, we don’t want to load them as they can<br>
simply have rate limiting implemented and they’ll at one moment block our request -> failure will occur.<br>
Hence we need to simulate request with cached data. If you look at files in `services folder` then they have cached data for such purposes. Also, in configs we need to have either separate config where caching is True or alter it manually

`Wrk` is a good benchmarking tool for load testing

Also, deployment is better done with `hypercorn` instead of ordinary deployment

```bash
Pip install hypercorn
hypercorn name of the running file without .py:app
Ex:
hypercorn app:app
```
