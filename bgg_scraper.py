#!/usr/bin/env python
# API Connector for boardgamegeek.com

import json
import requests
from time import sleep, perf_counter
from bs4 import BeautifulSoup


def hot_soup(path, parameters):
	response = requests.get(path, parameters)

	if '[200]' not in str(response):
		print('Response: {}\nRetrying in 5 seconds...'.format(response))
		sleep(5)
		response = requests.get(path, parameters)
		if '[200]' not in str(response):
			print('Response: {}\nRequest failed.'.format(response))

			return

	return BeautifulSoup(response.content, 'html.parser')


def game_data(game_id):
	root_path = 'https://www.boardgamegeek.com/xmlapi2/'
	parameters = {'id': game_id, 'stats': 1}
	path = root_path + 'thing'
	item = hot_soup(path, parameters).item

	if item:
		min_plr = item.minplayers['value']
		max_plr = item.maxplayers['value']
		min_pt = item.minplaytime['value']
		max_pt = item.maxplaytime['value']

		desc = item.description.string.replace('&#10;', '\n')
		desc = desc.replace('&mdash;', '-').replace('&ndash;', '-')
		desc = desc.replace('&hellip;', '...')

		return {
			'name': item.find('name', type='primary')['value'],
			'description': desc,
			'year': item.yearpublished['value'],
			'complexity': round(float(item.averageweight['value']), 1),
			'rating': round(float(item.average['value']), 1),
			'num_ratings': item.usersrated['value'],
			'url': 'https://boardgamegeek.com/boardgame/{}'.format(game_id),
			'image': item.contents[4].strip(),
			'thumbnail': item.thumbnail.string,
			'players': '{}-{}'.format(min_plr, max_plr) if min_plr != max_plr else max_plr,
			'playtime': '{}-{}'.format(min_pt, max_pt) if min_pt != max_pt else max_pt,
			'categories': [i['value'] for i in item.find_all(type='boardgamecategory')],
			'mechanics': [i['value'] for i in item.find_all(type='boardgamemechanic')]
		}


def request_collection():
	root_path = 'https://www.boardgamegeek.com/xmlapi2/'
	output = {}
	parameters = {'username': 'GreatOaksTavern'}
	path = root_path + 'collection'
	soup = hot_soup(path, parameters)
	items = soup.find_all('item')

	for item in items:
		name = item.find('name').string
		game_id = item['objectid']
		output[game_id] = name

	return output


def update_collection():
	bgg_coll = request_collection()
	with open('games.json', 'r+') as file:
		local_coll = json.load(file)

		for key in local_coll.keys():
			if key not in bgg_coll.keys():
				print('DELETED: {} ({})'.format(local_coll[key]['name'], key))
				del local_coll[key]

		for key in bgg_coll.keys():
			if key not in local_coll.keys():
				local_coll[key] = game_data(key)
				print('ADDED: {} ({})'.format(local_coll[key]['name'], key))

		file.seek(0)
		json.dump(local_coll, file, indent=4)
		file.truncate()


def collection_to_json():
	start = perf_counter()
	coll = request_collection()
	total = len(coll)
	count = 1

	for game_id in coll.keys():
		data = game_data(game_id)
		coll[game_id] = data
		f = (count, total, data['name'], game_id)
		print('Collecting #{f[0]} of {f[1]}: {f[2]} ({f[3]})'.format(f=f))
		count += 1
		sleep(5)

	with open('games.json', 'w') as file:
		json.dump(coll, file, indent=4)

	elapsed = perf_counter() - start
	elapsed_mins = round(elapsed / 60)
	elapsed_secs = elapsed % 60
	print('All Games Collected')
	print('Time Elapsed: {}m {}s'.format(elapsed_mins, elapsed_secs))


def main():
	update_collection()


if __name__ == "__main__":
	main()
