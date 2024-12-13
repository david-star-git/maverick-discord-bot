import discord
from discord import app_commands
from discord.ext import commands
import aiohttp
from datetime import datetime

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

                    # Get the current date for comparison
                    now = datetime.utcnow()

                    # Filter games that are truly free and have active promotions
                    current_free_games = [
                        game for game in free_games
                        if game.get("price", {}).get("totalPrice", {}).get("discountPrice", 0) == 0
                           and "freegames" in [category.get("path", "") for category in game.get("categories", [])]
                           and any(
                            promo.get("promotionalOffers") and any(
                                offer.get("startDate") and offer.get("endDate")
                                and datetime.strptime(offer["startDate"], "%Y-%m-%dT%H:%M:%S.000Z") <= now <= datetime.strptime(offer["endDate"], "%Y-%m-%dT%H:%M:%S.000Z")
                                for offer in promo.get("promotionalOffers", [])
                            ) for promo in game.get("promotions", {}).get("promotionalOffers", [])
                        )
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
                        game_end_dates = []

                        # Check if the game has any ongoing offers and include the end date if the offer has started
                        for promo in game.get("promotions", {}).get("promotionalOffers", []):
                            for offer in promo.get("promotionalOffers", []):
                                start_date = datetime.strptime(offer.get("startDate"), "%Y-%m-%dT%H:%M:%S.000Z")
                                end_date = datetime.strptime(offer.get("endDate"), "%Y-%m-%dT%H:%M:%S.000Z")

                                if start_date <= now <= end_date:
                                    game_end_dates.append(end_date.strftime("%Y-%m-%d %H:%M:%S UTC"))

                        # Add the offer end date to the embed if there's any
                        if game_end_dates:
                            embed.add_field(
                                name=name,
                                value=f"{description[:200]}...\n**Ends on:** {', '.join(game_end_dates)}\n[Get it here!]({url})",
                                inline=False
                            )
                        else:
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
