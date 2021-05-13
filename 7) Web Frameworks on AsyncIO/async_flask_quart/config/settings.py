import os
import json


def load(mode='dev') -> dict:
	file = os.path.join(os.path.dirname(__file__), f'{mode}.json')
	if not os.path.exists(file):
		raise Exception(f'Config not found for {mode}')

	with open(file, 'r', encoding='utf-8') as fl:
		return json.load(fl)
