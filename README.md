# Python Project Management CLI Tool

A command-line tool to manage users, projects, and tasks with JSON persistence.

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the environment:
   - Windows: `\.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

From the project root, use the CLI commands below.

### Add a user
```bash
python main.py add-user --name "Alex Johnson" --email alex@example.com
```

### List users
```bash
python main.py list-users
```

### Add a project
```bash
python main.py add-project --email alex@example.com --title "Website Redesign" --description "Update the landing page." --due-date 2026-07-15
```

### List projects
```bash
python main.py list-projects
```

### Show user projects
```bash
python main.py show-user-projects --email alex@example.com
```

### Add a task
```bash
python main.py add-task --project-id 1 --title "Design mockups" --status "in progress" --assigned-to "alex@example.com"
```

### List tasks
```bash
python main.py list-tasks
```

### Complete a task
```bash
python main.py complete-task --task-id 1
```

## Features

- Create and list users.
- Add projects assigned to users.
- Create tasks and assign them to project contributors.
- Mark tasks as completed.
- Persist data locally using JSON file storage.
- Pretty-print output with `rich`.

## Known Issues

- The tool relies on exact email matching for user lookups.
- Task assignment only accepts user emails; user IDs are not accepted directly.
- The CLI does not currently support removing users, projects, or tasks.

## Testing

Run unit tests with:
```bash
python -m unittest discover tests
```
