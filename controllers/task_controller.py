from models.task import Task

class TaskController:
    def __init__(self, db_manager) -> None:
        self.db=db_manager

    def add_task(self, title, description, priority, due_date, project_id, assignee_id) -> int:
        return self.db.add_task(Task(title,description,priority,due_date,project_id,assignee_id))

    def get_task(self, task_id):
        return self.db.get_task_by_id(task_id)

    def get_all_tasks(self):
        return self.db.get_all_tasks()

    def update_task(self, task_id, **kwargs):
        return self.db.update_task(task_id,**kwargs)

    def delete_task(self, task_id):
        return self.db.delete_task(task_id)

    def search_tasks(self, query):
        return self.db.search_tasks(query)

    def update_task_status(self, task_id, new_status):
        return self.db.update_task(task_id,status=new_status)

    def get_overdue_tasks(self):
        return [t for t in self.get_all_tasks() if t.is_overdue()]

    def get_tasks_by_project(self, project_id):
        return self.db.get_tasks_by_project(project_id)

    def get_tasks_by_user(self, user_id):
        return self.db.get_tasks_by_user(user_id)
