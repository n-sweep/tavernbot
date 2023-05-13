#!/usr/bin/env python
# Discord Bot cog!

import json
import discord
from discord.ext import commands

blue = 0x7289da
green = 0x43b581
yellow = 0xfaa61a
orange = 0xf04747


class AdminCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(pass_context=True, hidden=True)
	async def test(self, ctx):
		channels = ctx.guild.channels
		ch_names = [channel.name for channel in channels]
		roles = ctx.guild.roles
		role_names = [role.name for role in roles]
		print(ch_names)
		print(role_names)

	@commands.command(pass_context=True, hidden=True, aliases=['ignore'])
	async def ignore_channel(self, ctx):
		if str(self.bot.user.id) not in ctx.message.content:
			return

		with open(self.bot.config_fp, 'r+') as file:
			data = json.load(file)
			ch = ctx.channel
			if ch.id not in data['ignored_channels'].keys():
				data['ignored_channels'][ch.id] = {
					'name': ch.name,
					'server': {
						'name': ch.guild.name,
						'id': ch.guild.id
					}
				}

			await ctx.send("I will ignore messages in this channel.")

			file.seek(0)
			json.dump(data, file, indent=4)
			file.truncate()

	@commands.command(pass_context=True, hidden=True)
	async def init_reaction(self, ctx):
		if ctx.prefix != self.bot.config.get('admin_prefix'):
			return
		embed1 = discord.Embed(
			title="WELCOME TO **GREAT OAKS TAVERN**",
			description="Welcome to the fold. Consider yourself an honorary member of the Great Oaks Guild. Ask an admin for details about becoming a supporting member.",
			url="https://www.greatoakstavern.com",
			color=blue
		)
		embed1.add_field(
			name="SERVER RULES",
			value="- :one: Be excellent to one another\n- :two: Party on dudes\n\n**Don't be a Jerk!**\nThis channel serves as a hub for employees & as an online gathering space for many more. No matter why you’re here -- please be respectful.\n\n----",
			inline=False
		)
		embed1.add_field(
			name="Connect Outside of Discord",
			value="<:fb_logo:758798877024976987> https://facebook.com/greatoakstavern\n<:insta_logo:758800147114754090> https://instagram.com/greatoakstavern\n<:meetup_logo:758800373162180630> https://www.meetup.com/pro/greater-akron-board-games/\n\n----",
			inline=False
		)
		embed2 = discord.Embed(
			title="Acknowledgement",
			description="Once you have read and understood the rules and information above, please click the :white_check_mark: emoji at the bottom of this message to gain access to the server.\n\nThank you!",
			color=green
		)
		await ctx.send(embed=embed1)  # message.channel.history().flatten()
		msg = await ctx.send(embed=embed2)

		await msg.add_reaction('✅')

	@commands.command(pass_context=True, hidden=True)
	async def cleanup(self, ctx):
		if ctx.prefix != self.bot.config.get('admin_prefix'):
			return
		msg = ctx.message
		channel = msg.channel
		messages = await channel.history().flatten()
		for m in messages:
			if channel.name in ['testing-ground', 'general', 'welcome']:
				await m.delete()
			elif m.content.startswith('.'):
				await m.delete()

	@commands.command(pass_context=True, hidden=True)
	async def reload(self, ctx):
		if ctx.prefix != self.bot.config.get('admin_prefix'):
			return
		self.bot.load_config()
		self.bot.load_cogs(reload=True)

	@commands.command(pass_context=True, hidden=True)
	async def setgame(self, ctx, *args):
		output = []
		if args:
			for a in args:
				nocap = ['and', 'as', 'as if', 'as long as', 'at', 'but', 'by', 'even if', 'for', 'from', 'if', 'if only',
						 'in', 'into', 'like', 'near', 'now that', 'nor', 'of', 'off', 'on', 'on top of', 'once', 'onto',
						 'or', 'out of', 'over', 'past', 'so', 'so that', 'than', 'that', 'till', 'to', 'up', 'upon',
						 'with', 'when', 'yet']
				output.append(a if a in nocap else a[0].upper() + a[1:])
			output = ' '.join(output)
			if ctx.prefix != self.bot.config.get('admin_prefix'):
				text = '{}, eh? Sure, that sounds fun.'.format(output)
				await ctx.send(text)
		await self.bot.change_playing(output)


def setup(bot):
	bot.add_cog(AdminCog(bot))
