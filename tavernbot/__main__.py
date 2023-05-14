#!/usr/bin/env python
# Discord Bot Run Command!

import os
import logging
from bot.core import Bot

# https://discordapp.com/oauth2/authorize?client_id=ID_HERE&scope=bot&permissions=0

handler = logging.FileHandler('logs/session.log', encoding='utf-8', mode='w')


def main():
	d = os.path.dirname(os.path.realpath(__file__))
	bot = Bot(os.path.join(d, 'config/config.json'))
	bot.run(log_handler=handler, root_logger=True)


if __name__ == '__main__':
	main()
