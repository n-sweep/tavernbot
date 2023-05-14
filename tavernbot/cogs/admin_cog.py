#!/usr/bin/env python
# Discord Bot cog!

import logging

import discord
from discord.ext import commands

blue = 0x7289da
green = 0x43b581
yellow = 0xfaa61a
orange = 0xf04747


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        @bot.event
        async def on_raw_reaction_add(payload):
            memb = payload.member
            role = discord.utils.get(memb.guild.roles, name='Guest User')
            await memb.add_roles(role)
            logging.info(f'{memb.name} added to Guest Users')

    @commands.command(pass_context=True, hidden=True)
    async def test(self, ctx):
        logging.info('test')
        pass


async def setup(bot):
	await bot.add_cog(AdminCog(bot))
