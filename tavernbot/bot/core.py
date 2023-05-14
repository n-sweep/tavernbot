#!/usr/bin/env python
# Discord Bot!

import json
import asyncio
import logging
import traceback
from time import sleep

import discord
from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or

intents = discord.Intents.default()
intents.message_content = True


class Bot(commands.Bot):
    """
    Core Discord Bot
    """

    commands_list = {}

    def __init__(self, conf, connector=None):
        self.config_fp = conf
        self.load_config()
        self.token = self.config.get("token")
        super().__init__(
            command_prefix=when_mentioned_or(
                self.config.get("prefix"), self.config.get("admin_prefix")
            ),
            intents=intents,
        )
        asyncio.run(self.load_cogs())

    def run(self, **kwargs):
        """
        Run bot with token from config
        """
        super().run(self.token, **kwargs)

    def load_config(self):
        """
        Load configuration from given filepath
        """
        with open(self.config_fp, "r") as f:
            data = json.load(f)
            self.config = data

    async def load_cogs(self, reload=False):
        """
        Load cogs from configuration
        """
        for c in self.config.get("cogs"):
            logging.info(f'loading cog {c}')
            ext = "cogs." + c
            try:
                if reload:
                    await self.unload_extension(ext)
                await self.load_extension(ext)
            except Exception as e:
                logging.warn(e)
                try:
                    await self.unload_extension(ext)
                    await self.load_extension(ext)
                except Exception as e:
                    logging.exception("failed to import plugin {}".format(c))
                    raise

    @property
    def tag(self):
        return "<@{}>".format(self.user.id)

    async def change_playing(self, title=None):
        game = discord.Game(title) if title else None
        await self.change_presence(activity=game)

    async def typing(self, ctx, n=1):
        await ctx.trigger_typing()
        sleep(n)

    async def close(self):
        print("Closing {}...".format(self.user.name))
        await super().close()
