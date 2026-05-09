from models.user import User
from models.project import Project
from models.task import Task


# Test that a user can store a project
def test_user_can_add_project():
    user = User("Alex", "alex@email.com")
    project = Project("CLI Tool")

    user.add_project(project)

    assert len(user.projects) == 1
    assert user.projects[0].title == "CLI Tool"


# Test that a project can store a task
def test_project_can_add_task():
    project = Project("CLI Tool")
    task = Task("Build add-task command", "Alex")

    project.add_task(task)

    assert len(project.tasks) == 1
    assert project.tasks[0].title == "Build add-task command"


# Test that a task status changes to complete
def test_task_can_be_completed():
    task = Task("Write tests")

    task.mark_complete()

    assert task.status == "complete"


# Test that a user can find a project by title
def test_find_project():
    user = User("Sam")
    project = Project("Website")
    user.add_project(project)

    result = user.find_project("Website")

    assert result == project


# Test that a project can find a task by title
def test_find_task():
    project = Project("Website")
    task = Task("Create homepage")
    project.add_task(task)

    result = project.find_task("Create homepage")

    assert result == task