#!/usr/bin/env python
# Discord Bot cog!

import re
import os
import json
import discord
from discord.ext import commands
from random import randint, choice
from bgg import Collection

blue = 0x7289da
green = 0x43b581
yellow = 0xfaa61a
orange = 0xf04747

# todo: better die roller
# todo: draftlist / randraft with quick update
# todo: game search function


class Drafts:
	def __init__(self, filepath):
		self.fp = filepath
		self.draftlist = self.load_list()

	def load_list(self):
		with open(self.fp, 'r+') as file:
			return json.load(file)

	def commit_list(self):
		with open(self.fp, 'r+') as file:
			file.seek(0)
			json.dump(self.draftlist, file)
			file.truncate()

	def add(self, pos, draft):
		if pos:
			current = self.draftlist[pos - 1]
			if current != '-':
				return '**{0}** is already on handle **{1}**. Use `!replace {1} {2}` to replace it.'.format(current,
																											pos, draft)
			else:
				self.draftlist[pos - 1] = draft
				self.commit_list()
				return '**{}** added.'.format(draft)
		else:
			for i, d in enumerate(self.draftlist):
				if d == '-':
					self.draftlist[i] = draft
					self.commit_list()
					return '**{}** added.'.format(draft)

	def replace(self, pos, draft):
		current = self.draftlist[pos - 1]
		self.draftlist[pos - 1] = draft
		self.commit_list()
		return '**{}** has replaced **{}**.'.format(draft, current)

	def remove(self, pos):
		current = self.draftlist[pos - 1]
		self.draftlist[pos - 1] = '-'
		self.commit_list()
		return '**{}** removed from list.'.format(current)

	def clear(self):
		self.draftlist = ['-' for _ in range(12)]


class TavernCog(commands.Cog):

	def __init__(self, bot):
		self.bot = bot
		d = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
		self.collection = Collection(self.bot, os.path.join(d, 'games.json'))

	@commands.command(name='draftlist', description='List drinks on tap', pass_ctx=True, aliases=['draft', 'drafts', 'draftslist'])
	async def draftlist(self, ctx, *args):
		"""
		Return a list of drinks on draft at the bar
		"""

		d = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
		fp = os.path.join(d, 'draftlist.json')
		drafts = Drafts(fp)

		def drafts_embed(dlist):
			enumerated_drafts = ['- {}: **{}**'.format(i+1, d) for i, d in enumerate(dlist)]
			embed = discord.Embed(
				title=':beer: BEER ON DRAFT :beer:',
				description='\n'.join(enumerated_drafts),
				color=yellow
			)

			return embed

		if args:
			arg_lower = args[0].lower()

			if not (len(args) > 1 and arg_lower in ['add', 'replace', 'remove']):
				await ctx.send(embed=drafts_embed(drafts.draftlist))
				return

			pos = int(args[1]) if args[1].isdigit() else None
			draft = (' '.join(args[2:]) if pos else ' '.join(args[1:])) if len(args) > 2 else None

			if arg_lower == 'add':
				msg = drafts.add(pos, draft)
			elif arg_lower == 'replace':
				msg = drafts.replace(pos, draft)
			elif arg_lower == 'remove':
				msg = drafts.remove(pos)

			await ctx.send(msg)

		else:
			await ctx.send(embed=drafts_embed(drafts.draftlist))

	@commands.command(name='menu', description='Link to the GOT Menu', pass_ctx=True, aliases=['food'])
	async def menu(self, ctx):
		"""
		Return a link to our online menu.
		"""
		food_urls = [
			'https://images.squarespace-cdn.com/content/v1/5db20d8bf2603f171f9a9646/1576312114328-TIOJPF1FI5QVGYLZI1IY/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/IMG_0306+v2.jpg?format=500w',
			'https://images.squarespace-cdn.com/content/v1/5db20d8bf2603f171f9a9646/1576312084649-W90MBBSVDMIR3HFXI1KV/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/Copy+of+IMG_0389.JPG?format=500w',
			'https://images.squarespace-cdn.com/content/v1/5db20d8bf2603f171f9a9646/1576312085502-RL4PN828MGARISGRM6J6/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/Copy+of+IMG_0377.JPG?format=500w',
			'https://images.squarespace-cdn.com/content/v1/5db20d8bf2603f171f9a9646/1576312070441-9HSI93WX745ZVLF8K55A/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/Copy+of+IMG_0364.JPG?format=500w',
			'https://images.squarespace-cdn.com/content/v1/5db20d8bf2603f171f9a9646/1576312070617-EBSSPU2Z7V4FGNMN1L36/ke17ZwdGBToddI8pDm48kLkXF2pIyv_F2eUT9F60jBl7gQa3H78H3Y0txjaiv_0fDoOvxcdMmMKkDsyUqMSsMWxHk725yiiHCCLfrh8O1z4YTzHvnKhyp6Da-NYroOW3ZGjoBKy3azqku80C789l0iyqMbMesKd95J-X4EagrgU9L3Sa3U8cogeb0tjXbfawd0urKshkc5MgdBeJmALQKw/Copy+of+IMG_0319.JPG?format=500w'
		]
		embed = discord.Embed(
			title='Great Oaks Tavern **FULL MENU**',
			description='Check out our full menu online!',
			url='https://www.greatoakstavern.com/menu',
			color=orange
		)
		embed.set_thumbnail(url=choice(food_urls))

		await ctx.send(embed=embed)

	@commands.command(name='randomgame', description='Choose a random game from our collection', pass_ctx=True, aliases=['randgame'])
	async def randomgame(self, ctx, *args):
		"""
		Return a random game from the Great Oaks Collection
		"""
		await self.bot.typing(ctx)
		players = 0
		for arg in args:
			try:
				players = int(arg)
				break
			except:
				continue

		game = self.collection.random_game(players)
		paragraphs = game['description'].split('\n')
		plower = paragraphs[0].lower()
		if 'description' in plower or 'publisher' in plower:
			paragraphs = paragraphs.pop(0)
		desc = paragraphs[0]
		if len(desc) < 100:
			desc = desc + paragraphs[1]
		desc = desc.replace(game['name'], '***{}***'.format(game['name']))

		embed = discord.Embed(
			title='**{}** *({})*'.format(game['name'], game['year']),
			description=desc + '\n*(Read more at the link above.)*',
			url=game['url'] if game['url'] else game['thumbnail'],
			color=green,
		)
		embed.set_image(url=game['image'])
		embed.add_field(
			name='Number of Players',
			value=game['players'],
			inline=True
		)
		embed.add_field(
			name='Play Time',
			value=game['playtime'] + ' minutes',
			inline=True
		)
		embed.add_field(
			name='Categories',
			value=', '.join(game['categories']),
			inline=False
		)
		embed.add_field(
			name='Mechanics',
			value=', '.join(game['mechanics']),
			inline=False
		)
		footer = 'Complexity Rating: {}/5'.format(game['complexity'])
		embed.set_footer(
			text=footer,
			icon_url='https://images.squarespace-cdn.com/content/v1/5db20d8bf2603f171f9a9646/1593466725470-I9Y8GZMOYL0Z1H6YQDYJ/ke17ZwdGBToddI8pDm48kP06O0_IHyRXSOOiqwgWaApZw-zPPgdn4jUwVcJE1ZvWEtT5uBSRWt4vQZAgTJucoTqqXjS3CfNDSuuf31e0tVEsL0EX72Q6S7TgfQYQBQpkz5xM6Qt8VXd_xJGg_ziCFib8BodarTVrzIWCp72ioWw/favicon.ico?format=100w'
		)

		await ctx.send(embed=embed)

	@commands.command(name='roll', description='Rolls any number of dice and returns the total.',
					  pass_context=True, aliases=['dice', 'bones'])
	async def roll_dice(self, ctx, *args):
		"""
		Roll any number of dice provided in **d20** format. Returns the sum total of all dice rolled.
		"""
		caller = '<@!{}>'.format(ctx.message.author.id)

		def roll(die, rolls=1):
			total = 0
			for _ in range(rolls):
				total += randint(1, die)
			return total

		await self.bot.typing(ctx, .5)

		die_re = r'(?:(\d*)d)?(\d{1,3})'
		valid_sides = [4, 6, 8, 10, 12, 20, 100]
		dice = re.findall(die_re, ' '.join(args))
		results = []

		if dice:
			for r, d in dice:
				rolls = int(r) if r else 1
				die = int(d)
				if die not in valid_sides:
					text = "Sorry, I don't have any {}-sided dice.".format(die)
					await ctx.send(text)
					return
				results.append(roll(die, rolls))

			text = '{} rolled **{}**'.format(caller, sum(results))
			if len(dice) > 1:
				text += ' *({})*'.format(' + '.join([str(n) for n in results]))

			await ctx.send(text)

		elif args:
			await ctx.send('Sorry, I can only roll dice! Or try `!flip` to flip a coin.')

	@commands.command(description='Flip a coin!', pass_context=True, aliases=['flip', 'coin'])
	async def coinflip(self, ctx, coins=1):
		"""
		Flip a coin! Provide a number to flip multiple coins: **!flip n**.
		"""
		caller = '<@!{}>'.format(ctx.message.author.id)

		def flip():
			return choice(['Heads', 'Tails'])

		await self.bot.typing(ctx, .5)

		if coins > 1:
			flips = {}
			for _ in range(coins):
				result = flip()
				if result in flips:
					flips[result] += 1
				else:
					flips[result] = 1
			results = ' & '.join(['**{}** **{}**'.format(v, k) for k, v in flips.items()])
			output = '{} flipped {}'.format(caller, results)
		else:
			output = "{}'s coin came up **{}**".format(caller, flip())

		await ctx.send(output)


def setup(bot):
	bot.add_cog(TavernCog(bot))
