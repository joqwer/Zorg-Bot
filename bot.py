"""This is where the bot's main code is in."""

# Third Party Imports
import os
import logging
from dotenv import load_dotenv

# Discord.py
import discord
from discord.ext import commands

# First Party Imports
from utils.logging import logging_setup
from utils.cogs import load_cogs
from utils.db import init_db


def main() -> None:
    load_dotenv()

    root = logging_setup()

    TOKEN = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot('%', intents=intents)

    root.log(logging.INFO, 'Connecting to database...')

    database = init_db()['astral_bot']

    root.log(logging.INFO, f'Connected to database: {database.HOST}:{database.PORT}!')

    load_cogs(bot, root)

    @bot.event
    async def on_ready():
        """Prepares the bot when it is ready"""
        root.log(logging.INFO,
                 f'I am logged in as {bot.user.name}#{bot.user.discriminator}')

    @commands.is_owner()
    @bot.command()
    async def sync(ctx: commands.Context):
        """Syncronizes app commands with debug guild

        Args:
            ctx (commands.Context): The context of the interaction
        """
        guild = bot.get_guild(1091153826112872508)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        await ctx.send(f'Synced {len(synced)} commands to {guild.name}!')

    @commands.is_owner()
    @bot.command()
    async def syncglobal(ctx: commands.Context):
        """Syncronizes app commands gloablly

        Args:
            ctx (commands.Context): The context of the interaction
        """
        synced = await bot.tree.sync()
        await ctx.send(f'Synced {len(synced)} commands globally!')

    bot.run(TOKEN, log_handler=None)


if __name__ == '__main__':
    main()