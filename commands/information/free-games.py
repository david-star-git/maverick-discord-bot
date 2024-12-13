import discord
from discord import app_commands
from discord.ext import commands
import aiohttp

from imports.color_helper import get_user_color
from imports.permissions import has_permission

class FreeGamesCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="freegames", description="Fetches the current free games from the Epic Games Store.")
    async def freegames(self, interaction: discord.Interaction):
        command_name = "freegames"

        # Check if the user has permission to use this command
        if not has_permission(interaction.user.id, command_name):
            await interaction.response.send_message(
                content="You do not have permission to use this command.",
                ephemeral=True,
                delete_after=10
            )
            return

        async with aiohttp.ClientSession() as session:
            # Endpoint for Epic Games free games
            url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"

            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch data: HTTP {response.status}")

                    data = await response.json()
                    free_games = data.get("data", {}).get("Catalog", {}).get("searchStore", {}).get("elements", [])

                    # Filter games that are truly free (price is 0 and are in the "freegames" category)
                    current_free_games = [
                        game for game in free_games if game.get("price", {}).get("totalPrice", {}).get("discountPrice") == 0
                                                       and "freegames" in [category.get("path", "") for category in game.get("categories", [])]
                    ]

                    if not current_free_games:
                        await interaction.response.send_message(
                            content="No free games are currently available on the Epic Games Store.",
                        )
                        return

                    # Create embed for free games
                    embed = discord.Embed(
                        title="Free Games on Epic Games Store",
                        color=get_user_color(interaction.user.id),
                        description="Here are the currently free games!"
                    )

                    for game in current_free_games:
                        name = game.get("title", "Unknown Title")
                        description = game.get("description", "No description available.")
                        url = f"https://www.epicgames.com/store/p/{game.get('productSlug', '')}"
                        embed.add_field(
                            name=name,
                            value=f"{description[:200]}...\n[Get it here!]({url})",
                            inline=False
                        )

                    await interaction.response.send_message(embed=embed)

            except Exception as e:
                await interaction.response.send_message(
                    content=f"An error occurred while fetching free games: {e}",
                    ephemeral=True
                )

async def setup(bot):
    await bot.add_cog(FreeGamesCommand(bot))
