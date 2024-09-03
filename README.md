# Took

Took is a command-line tool for time tracking and task management, designed to help you efficiently manage and monitor the time spent on various tasks and projects. With Took, you can start, pause, and resume tasks, view detailed reports, and manage your time more effectively.  It's simple to set up and integrates seamlessly with your workflow.

## Features

- **Track Time:** Start tracking time for specific tasks, allowing you to keep a detailed log of how much time you spend on each task.
- **Pause and Resume:** Easily pause and resume tasks, ensuring that your time logs are accurate and reflect actual working hours.
- **Task Creation:** Automatically create tasks when starting time tracking for a task that doesn't exist.
- **Task Status:** View the status of all tasks, including time spent and the last time they were updated.
- **Task Logs:** Log time spent on tasks and store daily logs.
- **Daily Reports:** Generate reports to visualize the time spent on tasks over a specified number of days.
- **Persistent Storage:** All tasks and time logs are stored in a JSON file within the project directory, ensuring that your data is persistent across sessions and can be committed to the VCS.

## Installation

You can install Took using pip:

```bash
pip install took
```

## Usage

### Initialize a New Project

Before using Took, initialize it in your project directory:

```bash
$ took init
```

This command creates a `.took` directory and initializes the `took.json` file in the current directory.

### Start Tracking Time

To start tracking time for a task:

```bash
$ took start -t <task_name>
```

If the task doesn't already exist, it will be created automatically.

### Pause Tracking Time

To pause the currently active task:

```bash
$ took pause
```

### Resume a Paused Task

To resume tracking the paused task:

```bash
$ took start
```

This command will resume the most recently paused task.

### View Task Status

To view the current status of all tracked tasks, including time spent and last updated time:

```bash
$ took status
```

### View All Tracked Tasks

To see all tasks that are currently being tracked:

```bash
$ took show-all
```

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

## Contributing

We welcome contributions to Took! If you have suggestions, improvements, or bug fixes, please open an issue or submit a pull request on GitHub.

## License

Took is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
