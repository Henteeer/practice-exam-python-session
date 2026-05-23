from models.project import Project

class ProjectController:
    def __init__(self, db_manager):
        self.db=db_manager

    def add_project(self,name,description,start_date,end_date):
        return self.db.add_project(Project(name,description,start_date,end_date))

    def get_project(self,project_id):
        return self.db.get_project_by_id(project_id)

    def get_all_projects(self):
        return self.db.get_all_projects()

    def update_project(self,project_id,**kwargs):
        return self.db.update_project(project_id,**kwargs)

    def delete_project(self,project_id):
        return self.db.delete_project(project_id)

    def update_project_status(self,project_id,new_status):
        return self.db.update_project(project_id,status=new_status)

    def get_project_progress(self,project_id):
        p=self.get_project(project_id)
        return p.get_progress() if p else 0
