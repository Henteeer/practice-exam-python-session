
import sqlite3
from models.task import Task
from models.project import Project
from models.user import User
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="tasks.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self) -> None:
        self.conn.close()

    def create_tables(self) -> None:
        cur = self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT, description TEXT, priority INTEGER, status TEXT,
        due_date TEXT, project_id INTEGER, assignee_id INTEGER)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, description TEXT, start_date TEXT, end_date TEXT, status TEXT)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT, email TEXT, role TEXT, registration_date TEXT)""")
        self.conn.commit()

    def add_task(self, task: Task) -> int:
        cur=self.conn.cursor()
        cur.execute("INSERT INTO tasks(title,description,priority,status,due_date,project_id,assignee_id) VALUES(?,?,?,?,?,?,?)",
                    (task.title, task.description, task.priority, task.status, task.due_date.isoformat(), task.project_id, task.assignee_id))
        self.conn.commit()
        return cur.lastrowid

    def _row_to_task(self,row):
        if not row:return None
        t=Task(row['title'],row['description'],row['priority'],datetime.fromisoformat(row['due_date']),row['project_id'],row['assignee_id'])
        t.id=row['id']; t.status=row['status']; return t

    def get_task_by_id(self, task_id):
        row=self.conn.execute("SELECT * FROM tasks WHERE id=?",(task_id,)).fetchone()
        return self._row_to_task(row)

    def get_all_tasks(self):
        return [self._row_to_task(r) for r in self.conn.execute("SELECT * FROM tasks").fetchall()]

    def update_task(self, task_id, **kwargs):
        if not kwargs:return False
        if 'due_date' in kwargs and hasattr(kwargs['due_date'],'isoformat'):
            kwargs['due_date']=kwargs['due_date'].isoformat()
        q=", ".join(f"{k}=?" for k in kwargs)
        vals=list(kwargs.values())+[task_id]
        cur=self.conn.execute(f"UPDATE tasks SET {q} WHERE id=?",vals)
        self.conn.commit()
        return cur.rowcount>0

    def delete_task(self, task_id):
        cur=self.conn.execute("DELETE FROM tasks WHERE id=?",(task_id,))
        self.conn.commit(); return cur.rowcount>0

    def search_tasks(self, query):
        rows=self.conn.execute("SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?",(f"%{query}%",f"%{query}%")).fetchall()
        return [self._row_to_task(r) for r in rows]

    def get_tasks_by_project(self, project_id):
        rows=self.conn.execute("SELECT * FROM tasks WHERE project_id=?",(project_id,)).fetchall()
        return [self._row_to_task(r) for r in rows]

    def get_tasks_by_user(self, user_id):
        rows=self.conn.execute("SELECT * FROM tasks WHERE assignee_id=?",(user_id,)).fetchall()
        return [self._row_to_task(r) for r in rows]

    def add_project(self, project: Project):
        cur=self.conn.cursor()
        cur.execute("INSERT INTO projects(name,description,start_date,end_date,status) VALUES(?,?,?,?,?)",
                    (project.name,project.description,project.start_date.isoformat(),project.end_date.isoformat(),project.status))
        self.conn.commit(); return cur.lastrowid

    def _row_to_project(self,row):
        if not row:return None
        p=Project(row['name'],row['description'],datetime.fromisoformat(row['start_date']),datetime.fromisoformat(row['end_date']))
        p.id=row['id']; p.status=row['status']; return p

    def get_project_by_id(self, project_id):
        return self._row_to_project(self.conn.execute("SELECT * FROM projects WHERE id=?",(project_id,)).fetchone())

    def get_all_projects(self):
        return [self._row_to_project(r) for r in self.conn.execute("SELECT * FROM projects").fetchall()]

    def update_project(self, project_id, **kwargs):
        if not kwargs:return False
        for k in ('start_date','end_date'):
            if k in kwargs and hasattr(kwargs[k],'isoformat'): kwargs[k]=kwargs[k].isoformat()
        q=", ".join(f"{k}=?" for k in kwargs)
        vals=list(kwargs.values())+[project_id]
        cur=self.conn.execute(f"UPDATE projects SET {q} WHERE id=?",vals)
        self.conn.commit(); return cur.rowcount>0

    def delete_project(self, project_id):
        cur=self.conn.execute("DELETE FROM projects WHERE id=?",(project_id,))
        self.conn.commit(); return cur.rowcount>0

    def add_user(self, user: User):
        cur=self.conn.cursor()
        cur.execute("INSERT INTO users(username,email,role,registration_date) VALUES(?,?,?,?)",
                    (user.username,user.email,user.role,user.registration_date.isoformat()))
        self.conn.commit(); return cur.lastrowid

    def _row_to_user(self,row):
        if not row:return None
        u=User(row['username'],row['email'],row['role'])
        u.id=row['id']; u.registration_date=datetime.fromisoformat(row['registration_date']); return u

    def get_user_by_id(self, user_id):
        return self._row_to_user(self.conn.execute("SELECT * FROM users WHERE id=?",(user_id,)).fetchone())

    def get_all_users(self):
        return [self._row_to_user(r) for r in self.conn.execute("SELECT * FROM users").fetchall()]

    def update_user(self, user_id, **kwargs):
        if not kwargs:return False
        q=", ".join(f"{k}=?" for k in kwargs)
        vals=list(kwargs.values())+[user_id]
        cur=self.conn.execute(f"UPDATE users SET {q} WHERE id=?",vals)
        self.conn.commit(); return cur.rowcount>0

    def delete_user(self, user_id):
        cur=self.conn.execute("DELETE FROM users WHERE id=?",(user_id,))
        self.conn.commit(); return cur.rowcount>0
