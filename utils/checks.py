"""Discord check decorators"""
import discord
from discord.ext import commands
from discord import app_commands


def can_kick():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.kick_members
    return app_commands.check(predicate)


def can_ban():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.ban_members
    return app_commands.check(predicate)


def can_manage_messages():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.manage_messages
    return app_commands.check(predicate)


def can_manage_nicknames():
    """Returns the predicate"""
    def predicate(interaction: discord.Interaction) -> bool:
        """Checks if the user has the permission to kick members

        Args:
            interaction (discord.Interaction): The interaction that the bot makes

        Returns:
            bool: Returns true if permissions are met
        """
        return interaction.permissions.manage_nicknames
    return app_commands.check(predicate)

def check_hierarchy(member: discord.Member, user: discord.Member, guild: discord.Guild, bot: commands.Bot) -> bool:
    """Checks if user is high enough in the role hierarchy to perform an action

    Args:
        member (discord.Member): The victim
        user (discord.Member): The invocator
        guild (discord.Guild): The guild

    Returns:
        bool: Returns False if not authorized
    """
    if member.top_role >= user.top_role and user.id != guild.owner_id:
        return False
    if member.id in (guild.owner_id, bot.user.id):
        return False
    return True
    