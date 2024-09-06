import argparse
from datetime import datetime, timedelta
import json
import os
import sys
import took.ui as ui
import took.git_hooks as git_hooks
from took.constants import *

class TimeTracker:
    def __init__(self):
        """
        Initializes the TimeTracker object with default values. 
        - Initializes an empty task dictionary.
        - Sets the current task and root directory to None and pause state to False.
        """
        self.tasks = {}
        self.current_task = None
        self.paused = False
        self.root = None

    def init_file(self):
        """
        Initializes the JSON file for tracking tasks if it doesn't exist. 
        - Creates the directory and file structure for storing the task log.
        - Initializes the log with default values (empty tasks, no current task, and paused state).
        """
        if not os.path.exists(TOOK_DIR):
            os.makedirs(TOOK_DIR)
            with open(os.path.join(TOOK_DIR, FILE_NAME), 'w') as file:
                json.dump({
                    CURRENT: None,
                    TASKS: {},
                    PAUSED: False
                }, file, indent=4)
            print("Initialized new empty Took log in the current directory.")
        else:
            print("Took log already exists in this directory. No action taken.")
        
    def check_file(self):
        """
        Checks if the current or any parent directory contains a Took tracker project.
        - Searches upwards from the current directory.
        - If no Took directory is found, creates a global Took directory in the user's home directory.
        
        Returns:
            str: The path to the Took directory.
        """
        current_dir = os.getcwd()

        while True:
            if os.path.exists(os.path.join(current_dir, TOOK_DIR)):
                self.root = os.path.join(current_dir, TOOK_DIR)
                return self.root
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # reached the root without finding .took
                break
            current_dir = parent_dir

        home_dir = os.path.expanduser("~")
        central_took_dir = os.path.join(home_dir, TOOK_DIR)
        if not os.path.exists(central_took_dir):
            os.makedirs(central_took_dir)
            print(f"Created a global Took directory at {central_took_dir}")
            with open(os.path.join(central_took_dir, FILE_NAME), 'w') as file:
                json.dump({
                    CURRENT: None,
                    TASKS: {},
                    PAUSED: False
                }, file, indent=4)
            print("Initialized new empty Took log in the current directory.")
        self.root = central_took_dir
        return self.root
    
    def load_data(self):
        """
        Loads task data from the JSON file into the TimeTracker object.
        - Updates tasks, the current task, and the paused state based on the loaded data.
        """
        data = { CURRENT: None, TASKS:{} }
        if (self.root is not None) and os.path.exists(self.root):
            with open(os.path.join(self.root, FILE_NAME), 'r') as file:
                data = json.load(file)
        self.tasks = data[TASKS]
        self.current_task = data[CURRENT]
        self.paused = data[PAUSED]

    def save_data(self):
        """
        Saves the current state of tasks, the current task, and the paused state to the JSON file.
        """
        data = { CURRENT: self.current_task, TASKS: self.tasks, PAUSED: self.paused }
        with open(os.path.join(self.root, FILE_NAME), 'w') as file:
            json.dump(data, file, indent=4)

    def create_task(self, task_name):
        """
        Creates a new task in the tracker.
        
        Args:
            task_name (str): The name of the task to create.
        """
        self.tasks[task_name] = {
            TASK_NAME: task_name,
            LAST_UPDATED: None,
            TIME_SPENT: 0,
            LOG: {},
            DONE: False
        }
        print(f"Added '{task_name}' to tracked tasks")

    def refresh(self):
        """
        Updates the time spent on the current task by calculating the time elapsed since it was last updated.
        - If the task is not paused, it updates the daily logs and overall time spent.
        """
        if self.current_task is None:
            return
        current_task = self.tasks[self.current_task]
        last_updated = datetime.fromisoformat(current_task[LAST_UPDATED])
        now = datetime.now()

        if not self.paused:
            elapsed_time = now - last_updated
            seconds_spent = int(elapsed_time.total_seconds())

            # Iterate through each day between last_updated and now
            current_day = last_updated.date()
            end_day = now.date()

            while current_day <= end_day:
                date_str = current_day.isoformat()

                if current_day == last_updated.date():
                    # Calculate time from last_updated to end of that day
                    day_end = datetime.combine(current_day, datetime.max.time())
                    if day_end > now:
                        day_end = now
                    time_for_day = (day_end - last_updated).total_seconds()
                elif current_day == now.date():
                    # Calculate time from start of today to now
                    time_for_day = (now - datetime.combine(current_day, datetime.min.time())).total_seconds()
                else:
                    # Full day (24 hours)
                    time_for_day = 86400

                if date_str in current_task[LOG]:
                    current_task[LOG][date_str] += int(time_for_day)
                else:
                    current_task[LOG][date_str] = int(time_for_day)

                current_day += timedelta(days=1)

            current_task[TIME_SPENT] += seconds_spent
        current_task[LAST_UPDATED] = now.isoformat()

    def start_task(self, task_name):
        """
        Starts tracking a new or existing task.
        - If a task name is provided, it creates the task if it doesn't exist.
        - If no task is provided, it resumes the current task.
        
        Args:
            task_name (str): The name of the task to start.
        """
        if task_name is None:
            self.resume_task()
        else:
            self.paused = False
            if task_name not in self.tasks:
                self.create_task(task_name)
            now = datetime.now().isoformat()
            self.tasks[task_name][LAST_UPDATED] = now
            self.current_task = task_name
            print(f"Started tracking task: '{task_name}' at {now}")

    def pause_task(self):
        """
        Pauses the currently active task.
        - Prints a message if no task is running.
        """
        if self.current_task is None:
            print("No task is currently running. No action taken.")
            return
        self.paused = True
        print(f"Paused the current task '{self.current_task}'.")

    def resume_task(self):
        """
        Resumes a paused task.
        - If the current task is not paused or no task is paused, prints a warning message.
        """
        if self.current_task is None:
            print("No paused task to resume.")
            return
        if not self.paused:
            print(f"Current task {self.current_task} is not paused. No action taken.")
            return
        self.paused = False
        self.refresh()
        print(f"Resuming task '{self.current_task}'.")

    def remove_task(self, task_name):
        """
        Removes a task from the tracker.
        - If the removed task is the current task, stops tracking it.
        
        Args:
            task_name (str): The name of the task to remove.
        """
        if task_name in self.tasks:
            del self.tasks[task_name]
            print(f"Task '{task_name}' removed from tracked tasks.")
            if self.current_task == task_name:
                self.current_task = None
                self.pause = True
                print("No task is currently running.")
        else:
            print(f"Task '{task_name}' not found.")

    def done_task(self, task_name):
        """
        Marks a task as done.
        - Updates the task's status and stops tracking it if it's the current task.
        
        Args:
            task_name (str): The name of the task to mark as done.
        """
        if task_name in self.tasks:
            self.refresh()
            self.tasks[task_name][DONE] = True
            print(f"Task '{task_name}' marked as done.")
            if self.current_task == task_name:
                self.current_task = None
                self.pause = True
                print("No task is currently running.")
        else:
            print(f"Task '{task_name}' not found.")

    def format_time_spent(self, total_seconds):
        """
        Formats the total time spent on a task into a human-readable string.
        
        Args:
            total_seconds (int): Total number of seconds to format.
        
        Returns:
            str: A formatted string showing the time spent in years, months, days, hours, minutes, and seconds.
        """
        seconds_in_year = 60 * 60 * 24 * 365
        seconds_in_month = 60 * 60 * 24 * 30
        seconds_in_day = 60 * 60 * 24
        seconds_in_hour = 60 * 60
        seconds_in_minute = 60

        years, remainder = divmod(total_seconds, seconds_in_year)
        months, remainder = divmod(remainder, seconds_in_month)
        days, remainder = divmod(remainder, seconds_in_day)
        hours, remainder = divmod(remainder, seconds_in_hour)
        minutes, seconds = divmod(remainder, seconds_in_minute)

        parts = []
        if years > 0:
            parts.append(f"{years}Y-")
        if months > 0:
            parts.append(f"{months}M-")
        if days > 0:
            parts.append(f"{days}D-")
        if hours > 0:
            parts.append(f"{hours}h-")
        if minutes > 0:
            parts.append(f"{minutes}m-")
        if seconds > 0:
            parts.append(f"{seconds}s")

        return ''.join(parts) if parts else "0s"

    def show_status(self):
        """
        Displays the current status of all active tasks, including the time spent on each task.
        - If no tasks are logged, prints a message.
        """
        self.refresh()
        if len(self.tasks) == 0:
            print("No tasks logged.")
            return
        for entry in self.tasks.values():
            if not entry[DONE]:
                formatted_time_spent = self.format_time_spent(entry[TIME_SPENT])
                print(f"\n|Task: {entry[TASK_NAME]}\n|-Last Updated: {entry[LAST_UPDATED]} \n|-Time Spent: {formatted_time_spent}\n")


def main():
    """
    Main function to handle CLI commands using argparse.
    - Supports commands for initializing logs, starting, pausing, marking tasks as done, and more.
    - Executes the appropriate TimeTracker methods based on user input.
    """
    parser = argparse.ArgumentParser(description="Task Time Tracking Tool")
    subparsers = parser.add_subparsers(dest="command", required=False)

    init_parser = subparsers.add_parser('init', help="Initialize a tracking log in the current working directory.")
    init_parser.add_argument('--git',  help="Initialize Git Hooks to use took commands", action='store_true')

    start_aliases = ['s']
    start_parser = subparsers.add_parser('start', help="Start a new task.", aliases=start_aliases)
    start_parser.add_argument('-t','--task', type=str, help="The name of the task to start.")

    pause_aliases = ['p']
    subparsers.add_parser('pause', help="Pause the current task.", aliases=pause_aliases)

    done_parser = subparsers.add_parser('done', help="Mark a task as done.")
    done_parser.add_argument('-t', '--task', type=str, required=True, help="The name of the task to mark as done.")

    remove_aliases = ['rm']
    remove_parser = subparsers.add_parser('remove', help="Remove a tracked task.", aliases=remove_aliases)
    remove_parser.add_argument('-t', '--task', type=str, required=True, help="The name of the task to remove.")

    show_all_aliases = ['sa']
    show_all_parser = subparsers.add_parser('show-all', help="Show all tracked tasks.", aliases=show_all_aliases)
    show_all_parser.add_argument('--done',  help="Include tasks marked as done when showing all tasks", action='store_true')
    
    status_aliases = ['st']
    subparsers.add_parser('status', help="Show current status.", aliases=status_aliases)
    
    log_parser = subparsers.add_parser('log', help="Show the logged time per day for a given task.")
    log_parser.add_argument('-t','--task', type=str, help="The name of the task.")
    
    report_aliases = ['rp']
    report_parser = subparsers.add_parser('report', help="Report tracked time in the last {n} days.", aliases=report_aliases)
    report_parser.add_argument('-d', '--days', type=int, help="The number of days to be included in the report.")

    args = parser.parse_args()
    
    tt = TimeTracker()
    
    try:
        if args.command == "init":
            tt.init_file()
            if (args.git):
                git_hooks.init_git_hooks()
            sys.exit(0)
        else:
            tt.check_file()
            tt.load_data()
            tt.refresh()
            if args.command == "start" or args.command in start_aliases:
                tt.start_task(args.task)
            elif args.command == "pause" or args.command in pause_aliases:
                tt.pause_task()
            elif args.command == "done":
                tt.done_task(args.task)
            elif args.command == "remove" or args.command in remove_aliases:
                tt.remove_task(args.task)
            elif args.command == "status" or args.command in status_aliases:
                ui.show_status(tt)
            elif args.command == "show-all" or args.command in show_all_aliases:
                ui.show_all_tasks(tt, args.done)
            elif args.command == "log":
                ui.show_task_log(tt, args.task)
            elif args.command == "report" or args.command in report_aliases:
                ui.show_task_reports(tt, args.days)
            else:
                parser.print_help()
        tt.save_data()
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()
