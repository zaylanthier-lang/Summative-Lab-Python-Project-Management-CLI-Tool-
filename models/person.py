class Person:
    """Base class for people in the system."""

    def __init__(self, name, email=""):
        # Use setters so validation runs when object is created
        self.name = name
        self.email = email

    @property
    def name(self):
        """Return the person's name."""
        return self._name

    @name.setter
    def name(self, value):
        """Validate and set the person's name."""
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")

        self._name = value.strip()

    @property
    def email(self):
        """Return the person's email."""
        return self._email

    @email.setter
    def email(self, value):
        """Clean and set the person's email."""
        self._email = value.strip() if value else ""