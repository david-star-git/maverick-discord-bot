import discord
from discord import app_commands
from discord.ext import commands
from imports.task_manager import TaskManager
from imports.permissions import has_permission

class TaskModal(discord.ui.Modal, title="Add Task"):
    date = discord.ui.TextInput(
        label="Enter date (DD/MM):",
        placeholder="DD/MM",
        style=discord.TextStyle.short,
        required=True
    )
    message = discord.ui.TextInput(
        label="Enter task message:",
        placeholder="Task description",
        style=discord.TextStyle.long,
        required=True
    )

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
        self.interaction = interaction

    async def on_submit(self, interaction: discord.Interaction):
        # Retrieve the values from the modal
        task_date = self.date.value.strip()
        task_message = self.message.value.strip()

        # Check if the values are valid
        if not task_date or not task_message:
            await interaction.response.send_message(
                content="Both date and task message are required.",
                ephemeral=True
            )
            return

        # Try to add the task using TaskManager
        try:
            task_manager = TaskManager()
            task_manager.add_task(task_date, task_message)

            # Respond to user about task addition
            await interaction.response.send_message(
                content=f"Task for {task_date} has been successfully added!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                content=f"An error occurred while adding the task: {e}",
                ephemeral=True
            )

class TaskManagerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="add_task", description="Add a task for a specific date.")
    async def add_task(self, interaction: discord.Interaction):
        """Opens a modal where the user can input a date and message for the task."""
        # Check permissions
        command_name = "add_task"
        if not has_permission(interaction.user.id, command_name):
            await interaction.response.send_message(
                content="You do not have permission to use this command.",
                ephemeral=True,
                delete_after=10
            )
            return

        # Open the modal for adding a task
        await interaction.response.send_modal(TaskModal(interaction))

async def setup(bot):
    await bot.add_cog(TaskManagerCog(bot))
