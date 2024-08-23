# Took

Took is a command-line tool for time tracking and task management, designed to help you manage and monitor your time spent on various tasks and projects. With Took, you can track time, manage tasks, and visualize where your time goes with ease. It's simple to set up and integrates seamlessly with your workflow.

## Features

- **Track Time:** Log time spent on tasks and view detailed reports.
- **Pause and Resume:** Pause and resume tasks to accurately reflect your working hours.
- **Time Logs:** Export time logs and visualize them with rich CLI-based graphics.
- **Terminal Dashboard:** Use a terminal dashboard with graphical representations of your time logs.
- **Interactive Navigation:** Easily navigate through tasks and projects using an intuitive CLI interface.

## Installation

You can install Took using pip:

```bash
pip install took
```

## Usage

### Initialize a New Project

Before using Took, initialize it in your project directory:

```bash
took init
```

This command creates a `.took` directory and initializes the `time_log.json` file.

### Track Time

To start tracking time for a task:

```bash
took start <task_name>
```

To pause tracking time:

```bash
took pause
```

### View Task Status

View the current status of tracked tasks:

```bash
took status
```

### View Daliy Reports

To visualize time spent on each task per day:

```bash
took report {n_days}
```

## Contributing

We welcome contributions to Took! If you have suggestions, improvements, or bug fixes, please open an issue or submit a pull request on GitHub.

## License

Took is licensed under the MIT License. See [LICENSE](LICENSE) for more details.
