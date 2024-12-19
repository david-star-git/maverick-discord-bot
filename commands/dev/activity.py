import discord
import asyncio
import random
import json
from discord.ext import commands, tasks

CONFIG_PATH = "data/config.json"

# Helper function to load the "activity" from the configuration
def load_default_activity():
    try:
        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)
            return config.get("activity", "the pingwin eggs")  # Default to "the pingwin eggs"
    except (FileNotFoundError, json.JSONDecodeError):
        return "the pingwin eggs"

class RandomWatchingStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.custom_statuses = [
            "Minecraft gameplay",
            "your progress",
            "the stars",
            "cat videos",
            "how to be better",
            "buzi vagy sebi",
        ]  # List of custom statuses
        self.default_activity = load_default_activity()
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop()
    async def change_status(self):
        while True:
            interval = random.randint(1200, 7200)  # Random interval between 20 minutes (1200 seconds) and 2 hours (7200 seconds)
            await asyncio.sleep(interval)  # Wait for the random interval

            new_status = random.choice(self.custom_statuses)  # Select a random custom status
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=new_status))

            # Wait for 10 seconds before reverting
            await asyncio.sleep(10)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=self.default_activity))

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(RandomWatchingStatus(bot))
