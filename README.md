# Pingwin
**PINGWIN***

# TODO

[ ] pingwin.py -> add variety to messages
[ ] free-games.py -> set as bg process. also look for free games / promotions on steam ( once per day )

# Ideas

[ ] **Task scheduler**:
JSON File Structure: Instead of saving just MM/DD, save the full date in DD/MM/YYYY format:
```json
{
"01/01/2024": {"task": "New Year Celebration", "executed": false},
"25/12/2024": {"task": "Christmas Event", "executed": false}
}
```
Daily Check and Update: At the start of each day (or when the program starts), the program will:

Get the current date in DD/MM/YYYY format.
Check if there are any tasks for today in the JSON file.
Yearly Update:

If the program detects that the current year has changed, it can loop through all the tasks:
For each task with a date in the previous year (e.g., 01/01/2023), it will update the year part of the date to the current year (01/01/2024).
Mark all tasks for the new year as executed: false.
Task Execution:

If the task is for today and hasn't been executed ("executed": false), schedule it for 7 AM.
If the task is checked after 7 PM, execute it immediately.
Once executed, mark the task as "executed": true and save it back to the file.
Saving State: After checking, updating, and executing tasks, the program will save the updated JSON file, ensuring that all tasks for the current year are properly tracked.

Task Scheduling: Use schedule or APScheduler for scheduling tasks at 7 AM daily. When the year changes, the program can automatically handle task updates for the new year.

Example Code Concept:
When the program starts or daily, it checks if today’s date is in the JSON file.
If a task is due today, it will check if it has been executed. If not, execute it and update "executed": true.
At the start of a new year, loop through the stored tasks, update the year to the current year, and reset "executed": false for all tasks.