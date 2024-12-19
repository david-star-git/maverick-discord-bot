import json
import datetime
import os

class TaskManager:
    def __init__(self, task_file="data/tasks.json"):
        self.task_file = task_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Loads the tasks from the JSON file."""
        if os.path.exists(self.task_file):
            with open(self.task_file, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return {}

    def save_tasks(self):
        """Saves the tasks back to the JSON file with UTF-8 encoding."""
        with open(self.task_file, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def get_task_for_today(self, current_date=None):
        """Checks if there is a task for today. If yes, returns it."""
        if current_date is None:
            current_date = datetime.datetime.now()

        today = current_date.strftime("%d/%m/%Y")  # Format: DD/MM/YYYY

        # Update the year if it's the start of the year and update old tasks
        if current_date.month == 1 and current_date.day == 1:
            self.update_task_year(current_date.year)

        return self.tasks.get(today, None)

    def update_task_year(self, current_year):
        """Updates the year for all tasks to the current year if it has changed."""
        updated_tasks = {}
        for date_str, task_info in self.tasks.items():
            day_month = date_str.split('/')[0:2]
            updated_date = f"{day_month[0]}/{day_month[1]}/{current_year}"
            task_info['executed'] = False  # Reset executed flag for the new year
            updated_tasks[updated_date] = task_info

        self.tasks = updated_tasks
        self.save_tasks()

    def add_task(self, date, task, current_year=None):
        """Adds a new task to the task list."""
        if current_year is None:
            current_year = datetime.datetime.now().year
        task_date = f"{date}/{current_year}"
        self.tasks[task_date] = {"task": task, "executed": False}
        self.save_tasks()
