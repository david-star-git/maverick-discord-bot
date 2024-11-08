import discord
from discord import app_commands
from discord.ext import commands
from imports.permissions import has_permission

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="DEV: Responds with the bot's ping!")
    @app_commands.describe(visible="Whether the response should be visible to everyone.")
    async def ping(self, interaction: discord.Interaction, visible: str = "False"):
        command_name = "ping"

        # Check if the user has permission to use this command
        if has_permission(interaction.user.id, command_name):
            # Get the bot's latency
            ping = round(self.bot.latency * 1000)  # Convert to milliseconds

            # Determine the visibility of the response
            is_visible = visible.lower() == "true"

            # Send the response based on the visibility
            await interaction.response.send_message(
                content=f"Bot's ping is **{ping}**ms",
                ephemeral=not is_visible  # If visible is True, message is not ephemeral
            )
        else:
            # Inform the user that they do not have permission
            await interaction.response.send_message(
                content="You do not have permission to use this command.",
                ephemeral=True,
                delete_after=10
            )

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
