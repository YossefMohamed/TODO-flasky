from app.repositories.todo_repository import TodoRepository

class TodoService:
    @staticmethod
    def get_all_todos(user_id):
        return TodoRepository.get_all(user_id)

    @staticmethod
    def get_todo(todo_id, user_id):
        return TodoRepository.get_by_id(todo_id, user_id)

    @staticmethod
    def create_todo(task, user_id):
        return TodoRepository.create(task, user_id)

    @staticmethod
    def update_todo(todo_id, user_id, task=None, completed=None):
        todo = TodoRepository.get_by_id(todo_id, user_id)
        if todo:
            return TodoRepository.update(todo, task, completed)
        return None

    @staticmethod
    def delete_todo(todo_id, user_id):
        todo = TodoRepository.get_by_id(todo_id, user_id)
        if todo:
            TodoRepository.delete(todo)
            return True
        return False