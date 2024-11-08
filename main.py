import discord
import asyncio
import os
import json
import aiohttp
from discord.ext import commands
from imports.console import console
from imports.load_json import load_json

# Define bot intents for message content access
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

log_channel = "1296995020611784766"

# Create bot instance with command prefix and intents
client = commands.Bot(command_prefix="!", intents=intents)

# Load configuration and API credentials
config = load_json('config.json')
api = load_json('api.json')

async def load_cogs():
    """Load all cogs from the 'commands' directory and its subdirectories."""
    cogs_directory = "commands"
    for root, _, files in os.walk(cogs_directory):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                # Construct the cog path in dot notation
                cog_path = os.path.join(root, filename).replace(os.path.sep, ".")[:-3]
                try:
                    await client.load_extension(cog_path)
                    console.log(f"Successfully loaded {cog_path}.")
                except Exception as e:
                    console.error(f"Failed to load {cog_path}: {e}")

@client.event
async def on_ready():
    """Triggered when the bot has successfully connected to Discord."""
    await load_cogs()  # Load the Cogs
    console.log(f"Logged in as {str(client.user)[:-5]} (ID: {client.user.id})")

    # Synchronize application commands
    synced = await client.tree.sync()
    console.log(f"Synced {len(synced)} Commands")

    # Set the bot's activity status
    if 'activity' in config:
        await client.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name=config['activity'])
        )

async def main():
    # Check for TOKEN and start the bot
    if 'TOKEN' in api:
        await client.start(api['TOKEN'])
    else:
        console.error("Bot token not found in 'api.json'")

if __name__ == "__main__":
    try:
        # Run the async main function
        asyncio.run(main())
    except KeyboardInterrupt:
        console.success("Bot has been stopped.")
