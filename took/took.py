import argparse
from datetime import datetime
import json
import os
import sys
import took.ui

TOOK_DIR = ".took"
FILE_NAME = "took.json"
CURRENT = "current_task"
PAUSED = "paused"
TASKS = "tasks"
TASK_NAME = "task_name"
LAST_UPDATED = "last_updated"
TIME_SPENT = "time_spent"

class TimeTracker:
    def __init__(self):
      self.tasks = {}
      self.current_task = None
      self.paused = False
      self.root = None

    # Initialize the JSON file if it does not exist
    def init_file(self):
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
        sys.exit(0)
        

    # Check if the current directory or any parent directory is a tracker project
    def check_file(self):
        current_dir = os.getcwd()

        while True:
            if os.path.exists(os.path.join(current_dir, TOOK_DIR)):
                self.root = os.path.join(current_dir, TOOK_DIR)
                return self.root
            parent_dir = os.path.dirname(current_dir)
            if parent_dir == current_dir:  # reached the root without finding .took
                break
            current_dir = parent_dir
        
        print("Error: No .took directory found. Run `init` to create one.")
        sys.exit(1)
    
    def load_data(self):
      data = { CURRENT: None, TASKS:{} }
      if (self.root is not None) and os.path.exists(self.root):
          with open(os.path.join(self.root, FILE_NAME), 'r') as file:
              data = json.load(file)
      self.tasks = data[TASKS]
      self.current_task = data[CURRENT]
      self.paused = data[PAUSED]

    def save_data(self):
      data = { CURRENT: self.current_task, TASKS: self.tasks, PAUSED: self.paused }
      with open(os.path.join(self.root, FILE_NAME), 'w') as file:
        json.dump(data, file, indent=4)

    def create_task(self, task_name):
        self.tasks[task_name] = {
            TASK_NAME: task_name,
            LAST_UPDATED: None,
            TIME_SPENT: 0,
            "log": {}
        }
        print(f"Added '{task_name}' to tracked tasks")

    def refresh(self):
        if self.current_task is None:
            return
        current_task = self.tasks[self.current_task]
        last_updated = datetime.fromisoformat(current_task[LAST_UPDATED])
        now = datetime.now()
        if not self.paused:
            elapsed_time = now - last_updated
            seconds_spent = int(elapsed_time.total_seconds())
            current_task[TIME_SPENT] += seconds_spent
            # Log the time spent in the daily log
            date_str = last_updated.date().isoformat()
            if date_str in current_task["log"]:
                current_task["log"][date_str] += seconds_spent
            else:
                current_task["log"][date_str] = seconds_spent
        current_task[LAST_UPDATED] = now.isoformat()

        

    def start_task(self, task_name):
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

    def pause_task(self, ):
        if self.current_task is None:
            print("No task is currently running.")
            return
        self.paused = True
        print(f"Paused the current task '{self.current_task}'.")
    
    def resume_task(self):
        if self.current_task is None:
            print("No paused task to resume.")
            return
        if not self.paused:
            print(f"Current task {self.current_task} is not paused. No action taken.")
            return
        self.paused = False
        self.refresh()
        print(f"Resuming task '{self.current_task}'.")

    def format_time_spent(self, total_seconds):
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


    def show_status(self, ):
        self.refresh()
        if len(self.tasks) == 0:
            print("No tasks logged.")
            return
        for _i,entry in self.tasks.items():
            formatted_time_spent = self.format_time_spent(entry[TIME_SPENT])
            print(f"\n|Task: {entry[TASK_NAME]}\n|-Last Updated: {entry[LAST_UPDATED]} \n|-Time Spent: {formatted_time_spent}\n")



def main():
    parser = argparse.ArgumentParser(description="Task Time Tracking Tool")
    subparsers = parser.add_subparsers(dest="command", required=False)

    subparsers.add_parser('init', help="Initialize a tracking log in the current working directory.")

    start_aliases = ['s']
    start_parser = subparsers.add_parser('start', help="Start a new task.", aliases=start_aliases)
    start_parser.add_argument('-t','--task', type=str, help="The name of the task to start.")

    pause_aliases = ['p']
    subparsers.add_parser('pause', help="Pause the current task.", aliases=pause_aliases)

    show_all_aliases = ['sa']
    subparsers.add_parser('show-all', help="Show all tracked tasks.", aliases=show_all_aliases)
    
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
        else:
            tt.check_file()
            tt.load_data()
            tt.refresh()
            if args.command == "start" or args.command in start_aliases:
                tt.start_task(args.task)
            elif args.command == "pause" or args.command in pause_aliases:
                tt.pause_task()
            elif args.command == "status" or args.command in status_aliases:
                ui.show_status(tt)
            elif args.command == "show-all" or args.command in show_all_aliases:
                ui.show_all_tasks(tt)
            elif args.command == "log":
                ui.show_task_log(tt,args.task)
            elif args.command == "report" or args.command in report_aliases:
                ui.show_task_reports(tt, args.days)
            else:
                parser.print_help()
        tt.save_data()
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    main()


        
        