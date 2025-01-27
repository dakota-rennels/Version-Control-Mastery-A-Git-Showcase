import sys
import json
import logging
from pathlib import Path

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


def add_task(description):
    """Add a new task."""
    if not description.strip():
        logging.warning("Task description cannot be empty.")
        print("Error: Task description cannot be empty.")
        return
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "description": description.strip(),
        "completed": False
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task added: {description.strip()}")


def list_tasks():
    """List all tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks available. 🗒️ Start by adding one using `add` command.")
        return
    print("\n🗒️ Your Tasks:")
    print("-" * 30)
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        print(f"ID: {task['id']} | [{status}] {task['description']}")
    print("-" * 30)


def complete_task(task_id):
    """Mark a task as completed."""
    tasks = load_tasks()
    task_id = int(task_id)
    task_found = False
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"⚠️ Task {task_id} is already marked as completed.")
                return
            task["completed"] = True
            task_found = True
            save_tasks(tasks)
            print(f"✅ Task {task_id} completed: {task['description']}")
            return
    if not task_found:
        print(f"⚠️ Task ID {task_id} not found.")


def delete_task(task_id):
    """Delete a task."""
    tasks = load_tasks()
    task_id = int(task_id)
    filtered_tasks = [task for task in tasks if task["id"] != task_id]
    if len(tasks) == len(filtered_tasks):
        print(f"⚠️ Task ID {task_id} not found.")
        return
    for idx, task in enumerate(filtered_tasks, start=1):
        task["id"] = idx  # Reassign IDs after deletion
    save_tasks(filtered_tasks)
    print(f"🗑️ Task {task_id} deleted.")


def clear_all_tasks():
    """Clear all tasks."""
    confirmation = input("⚠️ Are you sure you want to delete all tasks? (y/n): ")
    if confirmation.lower() == "y":
        save_tasks([])
        print("🗑️ All tasks have been cleared.")
    else:
        print("Operation canceled.")


def print_help():
    """Display help text."""
    help_text = """
    ✅ CLI To-Do List Tool
    --------------------------------------
    Usage: python todo.py [command] [arguments]

    Commands:
        add [description]       Add a new task.
        list                    List all tasks.
        complete [id]           Mark a task as completed.
        delete [id]             Delete a specific task by ID.
        clear                   Delete all tasks.
        help                    Show this help message.

    Examples:
        python todo.py add "Buy groceries"
        python todo.py list
        python todo.py complete 1
        python todo.py delete 1
        python todo.py clear
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
                add_task(" ".join(sys.argv[2:]))
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
        elif command == "clear":
            clear_all_tasks()
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
