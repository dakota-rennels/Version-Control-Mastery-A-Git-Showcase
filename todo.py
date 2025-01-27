import sys
import json
import logging
from pathlib import Path
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("todo.log"),
        logging.StreamHandler()
    ]
)

# Define constants
TODO_FILE = Path("todo.json")

# Ensure the file exists
if not TODO_FILE.exists():
    logging.info(f"{TODO_FILE} not found. Creating an empty task file.")
    TODO_FILE.write_text(json.dumps([]))


def load_tasks():
    """Load tasks from the file."""
    try:
        with open(TODO_FILE, "r") as f:
            tasks = json.load(f)
            logging.info("Tasks successfully loaded from the file.")
            return tasks
    except json.JSONDecodeError:
        logging.error("Failed to decode tasks from the file. Resetting the file.")
        return []


def save_tasks(tasks):
    """Save tasks to the file."""
    try:
        with open(TODO_FILE, "w") as f:
            json.dump(tasks, f, indent=4)
            logging.info("Tasks successfully saved to the file.")
    except Exception as e:
        logging.error(f"Failed to save tasks: {e}")


def validate_date(date_str):
    """Validate the date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def add_task(description, deadline=None):
    """Add a new task."""
    if not description.strip():
        logging.warning("Task description cannot be empty.")
        print("Error: Task description cannot be empty.")
        return

    if deadline and not validate_date(deadline):
        print("❌ Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": description.strip(),
        "completed": False,
        "deadline": deadline.strip() if deadline else None
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: {description.strip()} {'(Deadline: ' + deadline + ')' if deadline else ''}")


def list_tasks():
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks available. 🗒️ Start by adding one using `add` command.")
        return
    print("\n🗒️ Your Tasks:")
    print("-" * 50)
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        deadline = f"(Deadline: {task['deadline']})" if task["deadline"] else ""
        print(f"ID: {task['id']} | [{status}] {task['description']} {deadline}")
    print("-" * 50)


def update_deadline(task_id, deadline):
    """Update the deadline of a specific task."""
    if not validate_date(deadline):
        print("❌ Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    tasks = load_tasks()
    task_found = False
    for task in tasks:
        if task["id"] == int(task_id):
            task["deadline"] = deadline
            task_found = True
            save_tasks(tasks)
            print(f"✅ Deadline updated for Task {task_id}: {deadline}")
            return
    if not task_found:
        print(f"⚠️ Task ID {task_id} not found.")


def print_help():
    """Display help text."""
    help_text = """
    ✅ CLI To-Do List Tool with Deadlines
    --------------------------------------
    Usage: python todo.py [command] [arguments]

    Commands:
        add [description] [deadline]  Add a new task with an optional deadline (YYYY-MM-DD).
        list                          List all tasks.
        complete [id]                 Mark a task as completed.
        delete [id]                   Delete a specific task by ID.
        update-deadline [id] [date]   Update the deadline of a specific task.
        help                          Show this help message.

    Examples:
        python todo.py add "Buy groceries" 2025-02-01
        python todo.py list
        python todo.py complete 1
        python todo.py delete 1
        python todo.py update-deadline 1 2025-03-01
    --------------------------------------
    """
    print(help_text)


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print_help()
            sys.exit(1)

        command = sys.argv[1].lower()
        if command == "add":
            if len(sys.argv) < 3:
                print("❌ Error: Task description required.")
            else:
                deadline = sys.argv[3] if len(sys.argv) > 3 else None
                add_task(" ".join(sys.argv[2:3]), deadline)
        elif command == "list":
            list_tasks()
        elif command == "complete":
            if len(sys.argv) < 3:
                print("❌ Error: Task ID required.")
            else:
                complete_task(sys.argv[2])
        elif command == "delete":
            if len(sys.argv) < 3:
                print("❌ Error: Task ID required.")
            else:
                delete_task(sys.argv[2])
        elif command == "update-deadline":
            if len(sys.argv) < 4:
                print("❌ Error: Task ID and deadline required.")
            else:
                update_deadline(sys.argv[2], sys.argv[3])
        elif command == "help":
            print_help()
        else:
            print(f"❌ Unknown command: {command}")
            print_help()
    except ValueError:
        print("❌ Error: Task ID must be a valid number.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error occurred: {e}")