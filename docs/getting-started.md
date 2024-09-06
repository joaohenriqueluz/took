## Installation

You can install Took using pip:

```bash
pip install took
```

## Usage

### Initialize a New Project

Before using `took`, initialize it in your project directory:

```bash
$ took init
```

This command creates a `.took` directory and initializes the `took.json` file in the current directory. If no `.took` directory is found in the current or parent directories, `took` will fall back to a central directory in your home folder to store tasks.

To set up Git hooks for automatic tracking with `took`:

```bash
$ took init --git
```

### Start Tracking Time

To start tracking time for a task:

```bash
$ took start -t <task_name>
```

If the task doesn't already exist, it will be created automatically. If you don’t specify a task name, `took` will resume the most recently paused task.

### Pause Tracking Time

To pause the currently active task:

```bash
$ took pause
```

Even when paused, `took` can retroactively track time if you forget to resume a task.

### Mark a Task as Done

To mark a task as done:

```bash
$ took done -t <task_name>
```

This marks the task as done and stops tracking time for it, but its logs will still be available.

### Remove a Task

To permanently remove a task from your tracked list:

```bash
$ took remove -t <task_name>
```

This deletes the task and its associated time logs.

### View Task Status

To view the current status of all active tasks, including time spent and the last updated time:

```bash
$ took status
```

This command only shows tasks that are still active (not completed).

### View All Tracked Tasks

To see all tasks being tracked, including both active and completed tasks:

```bash
$ took show-all --done
```

Use the `--done` option to include completed tasks.

### View Task Logs

To view the time logged per day for a specific task:

```bash
$ took log -t <task_name>
```

### Generate Daily Reports

To generate a report that shows the time spent on each task over the last `n` days:

```bash
$ took report -d {n_days}

╭───────────────────────╮
│ Reports (Last 3 Days) │
╰───────────────────────╯
2024-09-01
Task A: █████████████████████ 51m-7s
Task B: ███ 8m-53s
Task C: ████ 11m-7s

2024-09-02
Task A: ████████████████████ 11h-57m-47s
Task B: ██ 1h-47m-12s
Task C: ██████ 4h-10m-8s

2024-09-03
Task A: ██████ 27m-21s
Task B: █████ 20m-55s
Task C: ██████████████████ 1h-12m-47s
```

This report displays the time spent on each task over the given time period, broken down by day.
