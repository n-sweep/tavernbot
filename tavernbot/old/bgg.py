#!/usr/bin/env python
# Game Collection Interface

import json
from random import choice


class Collection:

	games = None

	def __init__(self, bot, data_filepath):
		self.bot = bot
		self.fp = data_filepath
		self.load_local_collection()

	def load_local_collection(self):
		with open(self.fp, 'r+') as file:
			self.games = json.load(file)

	def random_game(self, num_players=0):
		if num_players:
			games_list = []
			for gid, data in self.games.items():
				sp = [int(i) for i in data['players'].split('-')]
				if len(sp) > 1:
					if not sp[0] <= num_players <= sp[1]:
						continue
				else:
					if num_players != sp[0]:
						continue
				games_list.append(data)

			return choice(games_list)
		else:
			gid = choice(list(self.games.keys()))
			return self.games[gid]


def main():
	c = Collection('games.json')
	print(c.random_game(1))


if __name__ == '__main__':
	main()
