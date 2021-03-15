#!/usr/bin/env python
# Discord Bot!

import json
import traceback
from time import sleep

import discord
from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or


class Bot(commands.Bot):

	config = None
	commands_list = {}

	def __init__(self, conf, connector=None):
		self.config_fp = conf
		self.load_config()
		self.token = self.config.get('token')
		self.conn = connector
		super().__init__(command_prefix=when_mentioned_or(
			self.config.get('prefix'),
			self.config.get('admin_prefix')
		))
		self.load_cogs()

	def run(self):
		super().run(self.token)

	def load_config(self):
		with open(self.config_fp, 'r') as f:
			data = json.load(f)
			self.config = data

	def load_cogs(self, reload=False):
		for c in self.config.get('cogs'):
			ext = 'cogs.' + c
			try:
				if reload:
					self.unload_extension(ext)
				self.load_extension(ext)
			except Exception as e:
				print(e)
				try:
					self.unload_extension(ext)
					self.load_extension(ext)
				except Exception as e:
					print("failed to import plugin {}".format(c))
					traceback.print_tb(e.__traceback__)
					print(e)

	@property
	def tag(self):
		return '<@{}>'.format(self.user.id)

	async def change_playing(self, title=None):
		game = discord.Game(title) if title else None
		await self.change_presence(activity=game)

	async def typing(self, ctx, n=1):
		await ctx.trigger_typing()
		sleep(n)

	async def close(self):
		print('Closing {}...'.format(self.user.name))
		await super().close()
