#!/usr/bin/env python
# Discord Bot Run Command!

import os
from bot.core import Bot

# https://discordapp.com/oauth2/authorize?client_id=ID_HERE&scope=bot&permissions=0


def main():
	d = os.path.dirname(os.path.realpath(__file__))
	bot = Bot(os.path.join(d, 'config.json'))
	bot.run()


if __name__ == '__main__':
	main()
