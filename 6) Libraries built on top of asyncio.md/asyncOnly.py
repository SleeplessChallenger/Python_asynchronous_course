import datetime
import asyncio
import math
import aiohttp
import requests


def main():
	t0 = datetime.datetime.now()

	loop = asyncio.get_event_loop()

	tasks = [
        loop.create_task(compute_some()),
        loop.create_task(compute_some()),
        loop.create_task(compute_some()),
        loop.create_task(download_some()),
        loop.create_task(download_some()),
        loop.create_task(download_some_more()),
        loop.create_task(download_some_more()),
        loop.create_task(wait_some()),
        loop.create_task(wait_some()),
        loop.create_task(wait_some()),
        loop.create_task(wait_some()),
	]

	loop.run_until_complete(asyncio.gather(*tasks))

	dt = datetime.datetime.now() - t0
	print(f'Synchronous version done in {dt.total_seconds()}')

async def compute_some():
	print('Computing now!')
	for _ in range(1, 10_000_000):
		math.sqrt(25 ** 25 + .01)

async def download_some():
	print('Downloading now!')
	url = 'https://talkpython.fm/episodes/show/174/coming-into-python-from-another-industry-part-2'
	async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
		async with session.get(url) as resp:
			resp.raise_for_status()

			text = await resp.text()
	
	print(f'Downloaded {len(text)} characters')

async def download_some_more():
	print('Downloading more!!')
	url = 'https://pythonbytes.fm/episodes/show/92/will-your-python-be-compiled'
	resp = requests.get(url)
	resp.raise_for_status()

	text = resp.text
	print(f'Downloaded (more) {len(text)} characters')

async def wait_some():
	print('Waiting now!')
	for _ in range(1, 1000):
		await asyncio.sleep(.001)


if __name__ == '__main__':
	main()
