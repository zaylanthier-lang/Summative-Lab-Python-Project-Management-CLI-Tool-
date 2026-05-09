import argparse
from rich.console import Console
from rich.table import Table

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import load_users, save_users, find_user, find_project

# Console from Rich makes CLI output cleaner and more colorful
console = Console()


def add_user(args):
    """CLI command that adds a new user."""
    # Load saved users from JSON
    users = load_users()

    # Prevent duplicate users
    if find_user(users, args.name):
        console.print("[red]User already exists.[/red]")
        return

    # Create and save the new user
    user = User(args.name, args.email)
    users.append(user)
    save_users(users)

    console.print(f"[green]User added:[/green] {user.name}")


def list_users(args):
    """CLI command that lists all users."""
    # Load saved users from JSON
    users = load_users()

    # Build a Rich table for clean output
    table = Table(title="Users")
    table.add_column("Name")
    table.add_column("Email")
    table.add_column("Projects")

    # Add one row for each user
    for user in users:
        table.add_row(user.name, user.email or "None", str(len(user.projects)))

    console.print(table)


def add_project(args):
    """CLI command that adds a project to a user."""
    # Load saved users from JSON
    users = load_users()

    # Find the user who should receive the project
    user = find_user(users, args.user)

    if not user:
        console.print("[red]User not found.[/red]")
        return

    # Prevent duplicate project names for the same user
    if user.find_project(args.title):
        console.print("[red]Project already exists for this user.[/red]")
        return

    # Create and attach project to user
    project = Project(args.title, args.description, args.due_date)
    user.add_project(project)
    save_users(users)

    console.print(f"[green]Project added:[/green] {project.title}")


def list_projects(args):
    """CLI command that lists projects for a specific user."""
    # Load saved users from JSON
    users = load_users()

    # Find the requested user
    user = find_user(users, args.user)

    if not user:
        console.print("[red]User not found.[/red]")
        return

    # Build a Rich table for this user's projects
    table = Table(title=f"Projects for {user.name}")
    table.add_column("Title")
    table.add_column("Description")
    table.add_column("Due Date")
    table.add_column("Tasks")

    # Add one row for each project
    for project in user.projects:
        table.add_row(
            project.title,
            project.description or "None",
            project.due_date or "None",
            str(len(project.tasks))
        )

    console.print(table)


def add_task(args):
    """CLI command that adds a task to a project."""
    # Load saved users from JSON
    users = load_users()

    # Find the project across all users
    project = find_project(users, args.project)

    if not project:
        console.print("[red]Project not found.[/red]")
        return

    # Create and attach the new task to the project
    task = Task(args.title, args.assigned_to)
    project.add_task(task)
    save_users(users)

    console.print(f"[green]Task added:[/green] {task.title}")


def list_tasks(args):
    """CLI command that lists tasks for a project."""
    # Load saved users from JSON
    users = load_users()

    # Find the project across all users
    project = find_project(users, args.project)

    if not project:
        console.print("[red]Project not found.[/red]")
        return

    # Build a Rich table for the project's tasks
    table = Table(title=f"Tasks for {project.title}")
    table.add_column("Title")
    table.add_column("Assigned To")
    table.add_column("Status")

    # Add one row for each task
    for task in project.tasks:
        table.add_row(task.title, task.assigned_to or "None", task.status)

    console.print(table)


def complete_task(args):
    """CLI command that marks a task as complete."""
    # Load saved users from JSON
    users = load_users()

    # Find the project across all users
    project = find_project(users, args.project)

    if not project:
        console.print("[red]Project not found.[/red]")
        return

    # Find the task inside the project
    task = project.find_task(args.task)

    if not task:
        console.print("[red]Task not found.[/red]")
        return

    # Update task status and save changes
    task.mark_complete()
    save_users(users)

    console.print(f"[green]Task completed:[/green] {task.title}")


def main():
    """Main CLI entry point."""
    # Create the main parser for the app
    parser = argparse.ArgumentParser(description="Project Management CLI Tool")

    # Create subcommands like add-user, add-project, and add-task
    subparsers = parser.add_subparsers(dest="command")

    # add-user command
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", default="")
    add_user_parser.set_defaults(func=add_user)

    # list-users command
    list_users_parser = subparsers.add_parser("list-users", help="List all users")
    list_users_parser.set_defaults(func=list_users)

    # add-project command
    add_project_parser = subparsers.add_parser("add-project", help="Add project to user")
    add_project_parser.add_argument("--user", required=True)
    add_project_parser.add_argument("--title", required=True)
    add_project_parser.add_argument("--description", default="")
    add_project_parser.add_argument("--due-date", default="")
    add_project_parser.set_defaults(func=add_project)

    # list-projects command
    list_projects_parser = subparsers.add_parser("list-projects", help="List projects for user")
    list_projects_parser.add_argument("--user", required=True)
    list_projects_parser.set_defaults(func=list_projects)

    # add-task command
    add_task_parser = subparsers.add_parser("add-task", help="Add task to project")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--title", required=True)
    add_task_parser.add_argument("--assigned-to", default="")
    add_task_parser.set_defaults(func=add_task)

    # list-tasks command
    list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks for project")
    list_tasks_parser.add_argument("--project", required=True)
    list_tasks_parser.set_defaults(func=list_tasks)

    # complete-task command
    complete_task_parser = subparsers.add_parser("complete-task", help="Complete task")
    complete_task_parser.add_argument("--project", required=True)
    complete_task_parser.add_argument("--task", required=True)
    complete_task_parser.set_defaults(func=complete_task)

    # Read the user's command-line arguments
    args = parser.parse_args()

    # Run the correct function for the selected command
    if hasattr(args, "func"):
        args.func(args)
    else:
        # Show help if no command was entered
        parser.print_help()


# This makes sure main only runs when this file is executed directly
if __name__ == "__main__":
    main()