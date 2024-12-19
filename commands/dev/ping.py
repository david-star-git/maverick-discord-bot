import discord
import json
from discord import app_commands
from discord.ext import commands
from imports.permissions import has_permission

# Load and save config helpers
CONFIG_PATH = "data/config.json"

def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_config(data):
    with open(CONFIG_PATH, "w") as f:
        json.dump(data, f, indent=4)

# Special modal for delay input
class DelayModal(discord.ui.Modal, title="Set Delay"):
    delay = discord.ui.TextInput(
        label="Enter a delay (minutes)",
        placeholder="Enter a number between 5-60",
        min_length=1,
        max_length=2,  # Allow only two-digit numbers
        style=discord.TextStyle.short,
    )

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Validate and save the delay value
            delay_value = int(self.delay.value)
            if 5 <= delay_value <= 60:
                config = load_config()
                config["delay"] = delay_value
                save_config(config)

                await interaction.response.send_message(
                    content=f"Delay has been set to {delay_value} minutes.", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    content="Invalid input! Please enter a number between 5 and 60.", ephemeral=True
                )
        except ValueError:
            await interaction.response.send_message(
                content="Invalid input! Please enter a valid number.", ephemeral=True
            )

async def special_command_delay(interaction: discord.Interaction):
    if has_permission(interaction.user.id, "ping_delay"):
        await interaction.response.send_modal(DelayModal(interaction))

async def special_command_test(interaction: discord.Interaction):
    if has_permission(interaction.user.id, "ping_test"):
        await interaction.response.send_message(content="Test successful, you are in.", ephemeral=True)

async def handle_special_urls(url: str, interaction: discord.Interaction):
    # Map keywords to their corresponding command functions
    special_commands = {
        "test": special_command_test,
        "delay": special_command_delay
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
