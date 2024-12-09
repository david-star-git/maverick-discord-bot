import discord
from discord import app_commands
from discord.ext import commands
from imports.permissions import has_permission

async def special_command_test(interaction: discord.Interaction):
    if has_permission(interaction.user.id, "ping_test"):
        await interaction.response.send_message(content="Test successful, you are in.", ephemeral=True)

async def handle_special_urls(url: str, interaction: discord.Interaction):
    # Map keywords to their corresponding command functions
    special_commands = {
        "test": special_command_test
    }

    # Check if the URL matches any special keywords
    for keyword, command in special_commands.items():
        if url == keyword:
            # Check permissions for the corresponding command
            if has_permission(interaction.user.id, f"ping_{keyword}"):  # Check for api_ prefixed permission
                await command(interaction)  # Call the corresponding command function
                return True  # Indicate that a special response was sent
            else:
                return False  # User does not have permission for the special command
    return False  # No special response matched

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="DEV: Responds with the bot's ping!")
    @app_commands.describe(visible="Whether the response should be visible to everyone.")
    async def ping(self, interaction: discord.Interaction, visible: str = "False"):
        command_name = "ping"

        # Check if the user has permission to use this command
        if not has_permission(interaction.user.id, command_name):
            # Inform the user that they do not have permission
            await interaction.response.send_message(
                content="You do not have permission to use this command.",
                ephemeral=True,
                delete_after=10
            )
        else:
            if await handle_special_urls(visible, interaction):
                return
            
            # Get the bot's latency
            ping = round(self.bot.latency * 1000)  # Convert to milliseconds

            # Determine the visibility of the response
            is_visible = visible.lower() == "true"

            # Send the response based on the visibility
            await interaction.response.send_message(
                content=f"Bot's ping is **{ping}**ms",
                ephemeral=not is_visible  # If visible is True, message is not ephemeral
            )

async def setup(bot):
    await bot.add_cog(PingCommand(bot))
