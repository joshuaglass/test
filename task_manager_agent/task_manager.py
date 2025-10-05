class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: str):
        """Adds a task to the list."""
        self.tasks.append(task)
        return f"Task '{task}' added."

    def list_tasks(self):
        """Lists all tasks."""
        if not self.tasks:
            return "No tasks."
        return "\n".join(f"- {task}" for task in self.tasks)

    def clear_tasks(self):
        """Clears all tasks."""
        self.tasks = []
        return "All tasks cleared."