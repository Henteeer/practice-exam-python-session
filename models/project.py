class Project:
    VALID_STATUSES = ("active", "completed", "on_hold")

    def __init__(self, name, description, start_date, end_date) -> None:
        self.id = None
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = "active"

    def update_status(self, new_status) -> bool:
        if new_status not in self.VALID_STATUSES:
            return False
        self.status = new_status
        return True

    def get_progress(self) -> int:
        return 100.0 if self.status == "completed" else 0.0

    def to_dict(self) -> dict:
        return self.__dict__.copy()
