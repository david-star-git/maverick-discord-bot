import discord
from discord.ext import commands
import re

class PingwinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore the bot's own messages to prevent an endless loop
        if message.author == self.bot.user:
            return

        if re.search(r'\bpingwin\b', message.content, re.IGNORECASE):
            if 'pingwin!' in message.content.lower():
                await message.reply('Pingwin')
            if 'pingwin?' in message.content.lower():
                await message.reply('Pingwin!')
            else:
                await message.reply('Pingwin!')

        # Check if the specific user is mentioned
        if any(mention.id == 377185902998323203 for mention in message.mentions):
            await message.reply('Pingwin!')  # Respond with "Pingwin!" if the user is mentioned

            # Check if the specific user is mentioned
        if any(mention.id == 1304504215493804064 for mention in message.mentions):
            await message.reply('Spójrz! Jestem kurva pingwinem!')  # Respond with "Pingwin!" if the user is mentioned


# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(PingwinCog(bot))  # Add the cog correctly
