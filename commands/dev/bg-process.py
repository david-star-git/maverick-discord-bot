import discord
import asyncio
import random
import json
from discord.ext import commands, tasks

CONFIG_PATH = "data/config.json"

# Helper functions to load and save the delay configuration
def load_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"delay": 10}  # Default configuration

# Background process cog
class BackgroundProcess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_id = 690916913101930607  # Target server ID
        self.user_id = 424171739342307328    # Target user ID to monitor
        self.recipient_id = 377185902998323203  # Recipient user ID for DM
        self.check_voice_channels.start()

    def cog_unload(self):
        self.check_voice_channels.cancel()

    @tasks.loop(seconds=30)  # Checks every 30 seconds
    async def check_voice_channels(self):
        guild = self.bot.get_guild(self.server_id)
        recipient = self.bot.get_user(self.recipient_id)
        if not guild:
            return

        member = guild.get_member(self.user_id)
        if not member:
            return

        if member.voice:  # If the user is in a voice channel
            await recipient.send("Member is in voice channel.")
            config = load_config()
            delay_minutes = config.get("delay", 10)  # Default to 10 minutes
            await self.schedule_function(member, delay_minutes)

    async def schedule_function(self, member, delay_minutes):
        await asyncio.sleep(delay_minutes * 60)  # Wait for the delay period
        recipient = self.bot.get_user(self.recipient_id)
        if random.random() <= 0.3:  # 30% chance to execute the function
            if member.voice:
                if recipient:
                    try:
                        await recipient.send("The scheduled function has executed! And the user is still in a voice channel.")
                    except discord.Forbidden:
                        print(f"Failed to send DM to user {self.recipient_id}.")
            else:
                if recipient:
                    try:
                        await recipient.send("The scheduled function has executed! But the user is no longer in a voice channel.")
                    except discord.Forbidden:
                        print(f"Failed to send DM to user {self.recipient_id}.")

    @check_voice_channels.before_loop
    async def before_check_voice_channels(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(BackgroundProcess(bot))
