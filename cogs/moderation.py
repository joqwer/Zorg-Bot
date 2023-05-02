"""Contains general, but useful commands for the bot"""

import discord
from discord.ext import commands
from discord import app_commands
from utils.checks import can_kick, can_ban, can_mute


class Moderation(commands.Cog):
    """Cog for Moderation commands"""

    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot

    @app_commands.command(name='ban', description='Bans a user')
    @app_commands.describe(member='The member to ban.', reason='The reason for the ban', hidden='If the command is visible to the chat')
    @can_ban()
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = 'No reason provided', hidden: bool = False):
        """Bans the specified user (Only if author has ban perms)"""
        if reason == '':
            reason = 'No reason Provided'

        await member.ban(reason=reason + f' (Banned by {interaction.user.name}#{interaction.user.discriminator})')

        await interaction.response.send_message('Member has been banned', ephemeral=hidden)

    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.errors.CommandInvokeError):
            if str(error.__cause__) == '403 Forbidden (error code: 50013): Missing Permissions':
                await interaction.response.send_message('I do not have the permissions to do that!', ephemeral=True)

    @app_commands.command(name='kick', description='Kicks a user')
    @app_commands.describe(member='The member to kick.', reason='The reason for the kick', hidden='If the command is visible to the chat')
    @can_kick()
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = 'No reason provided', hidden: bool = False):
        """Kicks the specified user (Only if author has kick perms)"""
        if reason == '':
            reason = 'No reason Provided'

        await member.kick(reason=reason + f' (Banned by {interaction.user.name}#{interaction.user.discriminator})')

        await interaction.response.send_message('Member has been kicked', ephemeral=hidden)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        if isinstance(error, discord.app_commands.errors.CommandInvokeError):
            if str(error.__cause__) == '403 Forbidden (error code: 50013): Missing Permissions':
                await interaction.response.send_message('I do not have the permissions to do that!', ephemeral=True)


async def setup(bot: commands.Bot):
    """Sets up the cog

    Args:
        bot (commands.Bot): The bot logged in
    """
    await bot.add_cog(Moderation(bot))