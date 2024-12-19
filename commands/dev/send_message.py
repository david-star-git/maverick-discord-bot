import discord
from discord import app_commands
from discord.ext import commands

from imports.permissions import has_permission

# Special modal for message sending
class MessageModal(discord.ui.Modal, title="Send Message"):
    message = discord.ui.TextInput(
        label="Enter your message",
        placeholder="Enter a long message",
        style=discord.TextStyle.long,
        required=True
    )
    mention_id = discord.ui.TextInput(
        label="Optional: Mention ID",
        placeholder="Enter a mention ID (optional)",
        style=discord.TextStyle.short,
        required=False
    )
    channel_id = discord.ui.TextInput(
        label="Optional: Channel ID",
        placeholder="Enter a channel ID (optional)",
        style=discord.TextStyle.short,
        required=False
    )

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        message_content = self.message.value
        mention_id = self.mention_id.value.strip()
        channel_id = self.channel_id.value.strip()

        # Set default values if not provided
        if not channel_id:
            channel_id = 770755184245735475  # Default channel ID

        try:
            channel = self.interaction.guild.get_channel(int(channel_id))
            if not channel:
                await interaction.response.send_message(
                    content="Invalid channel ID. Could not find the channel.", ephemeral=True
                )
                return

            # If a mention ID is provided, prepend the message with a mention
            if mention_id:
                message_content = f"<@{mention_id}> {message_content}"

            await channel.send(message_content)

            await interaction.response.send_message(
                content="Message has been sent successfully.", ephemeral=True
            )

        except ValueError:
            await interaction.response.send_message(
                content="Invalid input! Please enter a valid number for channel or mention ID.", ephemeral=True
            )

class SendMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="send_message", description="DEV: Sends a message as the but user.")
    async def freegames(self, interaction: discord.Interaction):
        command_name = "send_message"

        # Check if the user has permission to use this command
        if not has_permission(interaction.user.id, command_name):
            await interaction.response.send_message(
                content="You do not have permission to use this command.",
                ephemeral=True,
                delete_after=10
            )
            return

        await interaction.response.send_modal(MessageModal(interaction))

async def setup(bot):
    await bot.add_cog(SendMessage(bot))
