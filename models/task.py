from datetime import datetime


class Task:
    VALID_STATUSES = ("pending", "in_progress", "completed")

    def __init__(self, title, description, priority, due_date, project_id, assignee_id) -> None:
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority
        self.status = "pending"
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status) -> bool:
        if new_status not in self.VALID_STATUSES:
            return False
        self.status = new_status
        return True

    def is_overdue(self) -> bool:
        return self.status != "completed" and self.due_date < datetime.now()

    def to_dict(self) -> dict:
        return self.__dict__.copy()
