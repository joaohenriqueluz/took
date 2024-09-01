import json
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from datetime import datetime, timedelta


CURRENT = "current_task"
TASKS = "tasks"
TASK_NAME = "task_name"
LAST_UPDATED = "last_updated"
TIME_SPENT = "time_spent"

# Display the status
def show_status(tt):
    console = Console()
    current_task = tt.current_task
    task_info = tt.tasks.get(current_task, {})
    
    if task_info:
        console.print(f"Current Task: {current_task}", style="bold green", end='') 
        if tt.paused:
            console.print(f" (paused)", style="red") 
        else:
            console.print(f" (in progress)", style="orange1") 
        formatted_time_spent = tt.format_time_spent(task_info[TIME_SPENT])
        console.print(f"Time Spent (s): {formatted_time_spent}")
        console.print(f"Last Updated: {task_info[LAST_UPDATED]}")
        

    else:
        console.print(f"No information available for current task: {current_task}")

def show_all_tasks(tt):
    console = Console()
    tasks = tt.tasks
    if not tasks:
        console.print(f"No tasks logged.")
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
        if key in tt.current_task:
            _style = "bold green"
            current_indicator = "*"

        formatted_time_spent = tt.format_time_spent(task[TIME_SPENT])
        table.add_row(current_indicator,
        task[TASK_NAME],
        formatted_time_spent,
        task[LAST_UPDATED],
        style=_style)
    
    if tt.paused:
        console.print(Panel("Took Tasks' Status", style="bold red", expand=False, subtitle="Paused"))
    else:
        console.print(Panel("Took Tasks' Status", style="bold blue", expand=False))
    console.print(table)

def show_task_log(tt, task_name):
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
    today = datetime.now().date()
    return [(today - timedelta(days=i)).isoformat() for i in range(n-1, -1, -1)]

def aggregate_time_per_day(tasks, dates):
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

