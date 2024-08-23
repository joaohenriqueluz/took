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

# Display the current task
def show_current_task(tt):
    console = Console()
    current_task = tt.current_task
    task_info = tt.tasks.get(current_task, {})
    
    if task_info:
        console.print(Panel(f"Current Task: {current_task}", style="bold green", expand=False))
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Task Name", style="dim", width=20)
        table.add_column("Last Updated", style="dim", width=30)
        table.add_column("Time Spent (s)", style="dim")
        table.add_row(
            task_info["task_name"],
            task_info["last_updated"],
            tt.format_time_spent(task_info["time_spent"])
        )
        console.print(table)
    else:
        console.print(f"No information available for current task: {current_task}")

# Display all tasks
def show_all_tasks(tt):
    console = Console()
    tasks = tt.tasks
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Task Name", style="dim", width=20)
    table.add_column("Last Updated", style="dim", width=30)
    table.add_column("Time Spent (s)", style="dim")
    
    for _, entry in tt.tasks.items():
        formatted_time_spent = tt.format_time_spent(entry[TIME_SPENT])
        table.add_row(entry[TASK_NAME], entry[LAST_UPDATED], formatted_time_spent)
        
        # Display the daily log
        console.print(f"Task: {entry[TASK_NAME]}")
        for date, seconds in sorted(entry["log"].items()):
            formatted_time = tt.format_time_spent(seconds)
            console.print(f"- {date}: {formatted_time}")


    
    console.print(Panel("All Tasks", style="bold blue", expand=False))
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

def show_task_reports(tt, n_days=7):
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

# Main function to navigate through tasks
def main(tt):
    console = Console()

    while True:
        console.print(Panel("Took UI", style="bold cyan", expand=False))
        console.print("1. View Current Task")
        console.print("2. View All Tasks")
        console.print("3. View Task Log")
        console.print("4. View Dashboard")
        console.print("5. Exit")
        
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6"])
        tt.refresh()
        if choice == "1":
            show_current_task(tt)
        elif choice == "2":
            show_all_tasks(tt)
        elif choice == "3":
            task_name = Prompt.ask("Enter task name")
            show_task_log(tt, task_name)
        elif choice == "4":
            show_task_reports(tt)
        elif choice == "5":
            console.print("Exiting...")
            break

# if __name__ == "__main__":
#     main()
