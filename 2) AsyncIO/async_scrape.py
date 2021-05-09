import aiohttp
import bs4
from colorama import Fore
import datetime
import asyncio
# start all the requests and then process
# when the responses start to come in

async def get_html(episode_number: int) -> str:
	print(Fore.YELLOW + f'Getting HTML for episode {episode_number}.',
		  flush=True)

	url = f'https://talkpython.fm/{episode_number}'
	# resp = requests.get(url)
	# resp.raise_for_status()
	# return resp.text

	# below we'll use asynchronous Context Manager
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as resp:
			resp.raise_for_status()

			return await resp.text()

def get_title(html: str, episode_number: int) -> str:
	print(Fore.CYAN + f'Getting TITLE for episode {episode_number}',
		  flush=True)
	soup = bs4.BeautifulSoup(html, 'html.parser')
	header = soup.select_one('h1')
	if not header:
		return 'Missing'

	return header.text.strip()

def main():
	t0 = datetime.datetime.now()
	global loop
	loop = asyncio.get_event_loop()
	
	loop.run_until_complete(get_title_range())

	dt = datetime.datetime.now() - t0
	print(f'Done in {dt.total_seconds():.2f} sec.')

async def get_title_range():
	# for not making DDoS attack, the range will be
	# kept within sane range
	tasks = []
	for n in range(120, 130):
		tasks.append((n, loop.create_task(get_html(n))))
		# start all the tasks and in next loop
		# either we receive all the tasks back
		# or wait for this response and switch
		# to another task

	for n, t in tasks:
		html = await t
		title = get_title(html, n)
		print(Fore.WHITE + f'Title found: {title}', flush=True)


if __name__ == '__main__':
	main()
