class Task:
    """Represents one task inside a project."""

    # Class attribute used to give every task a unique ID
    id_counter = 1

    def __init__(self, title, assigned_to="", status="incomplete", task_id=None):
        # If loading from JSON, reuse the saved ID. Otherwise create a new one.
        self.id = task_id if task_id else Task.id_counter

        # Keep the ID counter ahead of the largest existing ID
        Task.id_counter = max(Task.id_counter, self.id + 1)

        # Use the title setter so validation happens
        self.title = title

        # Person assigned to the task
        self.assigned_to = assigned_to

        # Task status starts as incomplete unless loaded differently
        self.status = status

    @property
    def title(self):
        """Return the task title."""
        return self._title

    @title.setter
    def title(self, value):
        """Validate and set the task title."""
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty.")

        self._title = value.strip()

    def mark_complete(self):
        """Mark this task as complete."""
        self.status = "complete"

    def to_dict(self):
        """Convert the task object into a dictionary for JSON saving."""
        return {
            "id": self.id,
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from saved dictionary data."""
        return cls(
            title=data["title"],
            assigned_to=data.get("assigned_to", ""),
            status=data.get("status", "incomplete"),
            task_id=data.get("id")
        )

    def __str__(self):
        """Return a clean string version of the task for the CLI."""
        return f"{self.title} | Assigned to: {self.assigned_to or 'None'} | Status: {self.status}"