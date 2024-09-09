"""
This module displays task tracking data with enhanced terminal output using the Rich library. 
It provides functions to show task status, logs, and reports based on time-tracked data 
from a `TimeTracker` instance.
"""

from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from took.constants import DONE, LAST_UPDATED, TASK_NAME, TIME_SPENT


# Display the status
def show_status(tt):
    """
    Displays the status of the current task.
    - Shows whether the task is paused or in progress.
    - Displays the time spent and the last update time.
    
    Args:
        tt (TimeTracker): An instance of the TimeTracker class containing task data.
    """
    console = Console()
    current_task = tt.current_task
    task_info = tt.tasks.get(current_task, {})

    if task_info:
        console.print(f"Current Task: {current_task}", style="bold green", end='')
        if tt.paused:
            console.print(" (paused)", style="red")
        else:
            console.print(" (in progress)", style="orange1")
        formatted_time_spent = tt.format_time_spent(task_info[TIME_SPENT])
        console.print(f"Time Spent (s): {formatted_time_spent}")
        console.print(f"Last Updated: {task_info[LAST_UPDATED]}")
    else:
        console.print(f"No information available for current task ({current_task}).")


def show_all_tasks(tt, include_done):
    """
    Displays a table with all tracked tasks.
    - Shows the task name, time spent, and the last update for each task.
    - Highlights the current task and can include or exclude completed tasks.
    
    Args:
        tt (TimeTracker): An instance of the TimeTracker class containing task data.
        include_done (bool): Whether to include tasks marked as done in the output.
    """
    console = Console()
    tasks = tt.tasks
    if not tasks:
        console.print("No tasks logged.")
        return
    table_style = "dim" if tt.paused else ""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("", style=table_style, width=1)
    table.add_column("Task Name", style=table_style, width=20)
    table.add_column("Time Spent (s)", style=table_style)
    table.add_column("Last Updated", style=table_style, width=30)

    for key, task in tt.tasks.items():
        _style = ""
        current_indicator = ""
        task_name = task[TASK_NAME]
        if (tt.current_task is not None) and (key == tt.current_task):
            _style = "bold green"
            current_indicator = "*"
        if task[DONE]:
            if include_done:
                _style = "dim"
                task_name = "(done) " + task_name
            else:
                continue
        formatted_time_spent = tt.format_time_spent(task[TIME_SPENT])
        table.add_row(current_indicator,
        task_name,
        formatted_time_spent,
        task[LAST_UPDATED],
        style=_style)

    if tt.paused:
        console.print(Panel("Took Tasks' Status", style="bold red", expand=False, subtitle="Paused"))
    else:
        console.print(Panel("Took Tasks' Status", style="bold blue", expand=False))
    console.print(table)


def show_task_log(tt, task_name):
    """
    Displays the log of time spent on a specific task, with a breakdown by day.
    
    Args:
        tt (TimeTracker): An instance of the TimeTracker class containing task data.
        task_name (str): The name of the task whose log will be displayed.
    """
    console = Console()
    task = tt.tasks.get(task_name)
    if not task:
        console.print(f"No task found with the name '{task_name}'", style="bold red")
        return
    console.print(Panel(f"Task Log for: {task_name}", style="bold green", expand=False))
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Date", style="dim", width=20)
    table.add_column("Time Spent", style="dim")

    for date, seconds in sorted(task["log"].items()):
        formatted_time = tt.format_time_spent(seconds)
        table.add_row(date, formatted_time)

    console.print(table)


def get_previous_days(n):
    """
    Returns a list of the last 'n' days, including today.
    
    Args:
        n (int): The number of days to include.
    
    Returns:
        list: A list of dates in ISO format, starting from today and going back 'n' days.
    """
    today = datetime.now().date()
    return [(today - timedelta(days=i)).isoformat() for i in range(n-1, -1, -1)]


def aggregate_time_per_day(tasks, dates):
    """
    Aggregates the time spent on all tasks per day.
    
    Args:
        tasks (dict): A dictionary of all tasks with their logs.
        dates (list): A list of dates for which to aggregate the time.
    
    Returns:
        dict: A dictionary with dates as keys and the time spent per task for each day.
    """
    daily_totals = {date: {} for date in dates}
    for task_name, task in tasks.items():
        for date, seconds in task["log"].items():
            if date in daily_totals:
                if task_name in daily_totals[date]:
                    daily_totals[date][task_name] += seconds
                else:
                    daily_totals[date][task_name] = seconds
    return daily_totals


def show_task_reports(tt, n_days):
    """
    Displays a report of time spent on tasks over the last 'n_days'.
    - Shows each day, with a bar graph of the time spent on each task.
    
    Args:
        tt (TimeTracker): An instance of the TimeTracker class containing task data.
        n_days (int): The number of days to include in the report.
    """
    if not n_days:
        n_days = 1
    console = Console()
    console.print(Panel(f"Reports (Last {n_days} Days)", style="bold blue", expand=False))

    dates = get_previous_days(n_days)
    daily_totals = aggregate_time_per_day(tt.tasks, dates)

    max_bar_length = 30  # Adjust the length of the bar graph

    for date in dates:
        console.print(f"[bold yellow]{date}[/bold yellow]")
        day_total_seconds = sum(daily_totals[date].values())

        for task_name, seconds in daily_totals[date].items():
            bar_length = int((seconds / day_total_seconds) * max_bar_length) if day_total_seconds > 0 else 0
            bar = Text("█" * bar_length, style="green")
            formatted_time = tt.format_time_spent(seconds)
            console.print(f"{task_name}: {bar} {formatted_time}")

        console.print("")
