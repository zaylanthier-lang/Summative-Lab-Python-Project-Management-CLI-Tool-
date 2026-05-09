from models.task import Task


class Project:
    """Represents one project that can contain many tasks."""

    # Class attribute used to give every project a unique ID
    id_counter = 1

    def __init__(self, title, description="", due_date="", tasks=None, project_id=None):
        # If loading from JSON, reuse the saved ID. Otherwise create a new one.
        self.id = project_id if project_id else Project.id_counter

        # Keep the ID counter ahead of the largest existing ID
        Project.id_counter = max(Project.id_counter, self.id + 1)

        # Use the title setter so validation happens
        self.title = title

        # Extra project information
        self.description = description
        self.due_date = due_date

        # One-to-many relationship: one project has many tasks
        self.tasks = tasks if tasks else []

    @property
    def title(self):
        """Return the project title."""
        return self._title

    @title.setter
    def title(self, value):
        """Validate and set the project title."""
        if not value or not value.strip():
            raise ValueError("Project title cannot be empty.")

        self._title = value.strip()

    def add_task(self, task):
        """Add a task object to this project."""
        self.tasks.append(task)

    def find_task(self, task_title):
        """Find and return a task by title."""
        for task in self.tasks:
            if task.title.lower() == task_title.lower():
                return task

        return None

    def to_dict(self):
        """Convert the project object into a dictionary for JSON saving."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Project object from saved dictionary data."""
        # Rebuild each saved task as a Task object
        tasks = [Task.from_dict(task) for task in data.get("tasks", [])]

        return cls(
            title=data["title"],
            description=data.get("description", ""),
            due_date=data.get("due_date", ""),
            tasks=tasks,
            project_id=data.get("id")
        )

    def __str__(self):
        """Return a clean string version of the project for the CLI."""
        return f"{self.title} | Due: {self.due_date or 'No due date'}"