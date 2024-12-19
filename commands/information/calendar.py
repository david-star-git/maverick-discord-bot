import discord
from discord import app_commands
from discord.ext import commands
import json
import datetime
from imports.permissions import has_permission
from imports.color_helper import get_user_color

class CalendarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="calendar", description="Show tasks for the current year that need to be completed.")
    async def calendar(self, interaction: discord.Interaction):
        """Returns an embed with tasks that need to be completed, grouped by month."""
        # Check permissions
        command_name = "calendar"
        if not has_permission(interaction.user.id, command_name):
            await interaction.response.send_message(
                content="You do not have permission to use this command.",
                ephemeral=True,
                delete_after=10
            )
            return

        # Get today's date
        current_year = datetime.datetime.now().year
        tasks_by_month = {}

        # Fetch tasks from tasks.json file
        try:
            # Load tasks from tasks.json
            with open('data/tasks.json', 'r', encoding="utf-8") as file:
                tasks = json.load(file)

            # Iterate over tasks and group by month
            for task_date, task_info in tasks.items():
                task_message = task_info.get("task")
                if task_message:
                    try:
                        # Ensure the task date is in DD/MM/YYYY format
                        day, month, year = task_date.split("/")
                        month = int(month)
                        day = int(day)
                        year = int(year)

                        # Only show tasks for the current year
                        if year != current_year:
                            continue

                        # Truncate message to max 40 characters
                        truncated_message = (task_message[:40] + "...") if len(task_message) > 40 else task_message

                        # Group by month
                        if month < 1 or month > 12:
                            continue  # Skip invalid months
                        if month not in tasks_by_month:
                            tasks_by_month[month] = []  # Initialize empty list if month not exists
                        tasks_by_month[month].append(f"{day}: {truncated_message}")

                    except ValueError:
                        continue  # Skip any tasks with invalid date formats

            # Create the embed to display the tasks
            embed = discord.Embed(
                title=f"Tasks for {current_year}",
                description="Here is the current state of the calendar.",
                color=get_user_color(interaction.user.id),  # Ensure you have this function defined
            )

            # Add tasks to the embed, grouped by month
            for month, tasks in tasks_by_month.items():
                month_name = datetime.datetime(current_year, month, 1).strftime("%B")
                # Ensure that task content is properly encoded to UTF-8 for display in the embed
                encoded_tasks = "\n".join(tasks)
                embed.add_field(name=f"{month_name}:", value=encoded_tasks, inline=False)

            # Send the embed
            await interaction.response.send_message(embed=embed)

        except FileNotFoundError:
            await interaction.response.send_message(
                content="The tasks file was not found.",
                ephemeral=True,
                delete_after=10
            )
        except json.JSONDecodeError:
            await interaction.response.send_message(
                content="There was an error decoding the tasks file.",
                ephemeral=True,
                delete_after=10
            )
        except Exception as e:
            await interaction.response.send_message(
                content=f"An error occurred while fetching tasks: {e}",
                ephemeral=True,
                delete_after=10
            )

async def setup(bot):
    await bot.add_cog(CalendarCog(bot))
