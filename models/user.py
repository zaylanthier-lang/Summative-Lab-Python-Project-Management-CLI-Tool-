from models.person import Person
from models.project import Project


class User(Person):
    """Represents one user who can own many projects."""

    # Class attribute used to give every user a unique ID
    id_counter = 1

    def __init__(self, name, email="", projects=None, user_id=None):
        # Call the parent Person class to set name and email
        super().__init__(name, email)

        # If loading from JSON, reuse the saved ID. Otherwise create a new one.
        self.id = user_id if user_id else User.id_counter

        # Keep the ID counter ahead of the largest existing ID
        User.id_counter = max(User.id_counter, self.id + 1)

        # One-to-many relationship: one user has many projects
        self.projects = projects if projects else []

    def add_project(self, project):
        """Add a project object to this user."""
        self.projects.append(project)

    def find_project(self, project_title):
        """Find and return a project by title."""
        for project in self.projects:
            if project.title.lower() == project_title.lower():
                return project

        return None

    def to_dict(self):
        """Convert the user object into a dictionary for JSON saving."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "projects": [project.to_dict() for project in self.projects]
        }

    @classmethod
    def from_dict(cls, data):
        """Create a User object from saved dictionary data."""
        # Rebuild each saved project as a Project object
        projects = [Project.from_dict(project) for project in data.get("projects", [])]

        return cls(
            name=data["name"],
            email=data.get("email", ""),
            projects=projects,
            user_id=data.get("id")
        )

    def __str__(self):
        """Return a clean string version of the user for the CLI."""
        return f"{self.name} | Email: {self.email or 'No email'}"