#!/usr/bin/env python
# Discord Bot cog!

import logging

import discord
from discord.ext import commands

blue = 0x7389da
green = 0x43b581
yellow = 0xfaa61a
orange = 0xf04747


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.event
        async def on_ready():
            logging.info('\nLogged in as')
            logging.info(bot.user.name)
            logging.info(bot.user.id)
            logging.info('Discord.py Version: {}'.format(discord.__version__))
            logging.info('--------\n')

    @commands.command(description='Pings the bot and returns the latency in seconds.', pass_context=True, hidden=True)
    async def ping(self, ctx):
        """
        Pings the bot and returns the latency in seconds.
        """

        latency = self.bot.latency
        await ctx.send('!pong ({})'.format(latency))

    @commands.command(description='Returns an info card for the bot.', pass_context=True)
    async def info(self, ctx):
        embed = discord.Embed(title="**{}**".format(self.bot.config['name']),
                             description=self.bot.config['description'],
                              color=yellow)
        embed.add_field(name='Author', value='<@{}>'.format(self.bot.config['author']))
        embed.add_field(name='Commands', value='I can respond to some commands, type **!commands** for a list.',
                        inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(MainCog(bot))
