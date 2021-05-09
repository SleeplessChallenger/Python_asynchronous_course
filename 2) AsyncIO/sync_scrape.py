import requests
import bs4
from colorama import Fore
import datetime


def get_html(episode_number: int) -> str:
	print(Fore.YELLOW + f'Getting HTML for episode {episode_number}.',
		  flush=True)

	url = f'https://talkpython.fm/{episode_number}'
	resp = requests.get(url)
	resp.raise_for_status()
	# (above) returns an HTTPError
	# object if an error has occurred
	return resp.text

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
	get_title_range()
	dt = datetime.datetime.now() - t0
	print(f'Done in {dt.total_seconds():.2f} sec.')

def get_title_range():
	# for not making DDoS attack, the range will be
	# kept within sane range
	for n in range(130, 155):
		html = get_html(n)
		title = get_title(html, n)
		print(Fore.WHITE + f'Title found: {title}',
			  flush=True)


if __name__ == '__main__':
	main()
