from app import db
from app.models.todo import Todo

class TodoRepository:
    @staticmethod
    def get_all(user_id):
        return Todo.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_by_id(todo_id, user_id):
        return Todo.query.filter_by(id=todo_id, user_id=user_id).first()

    @staticmethod
    def create(task, user_id):
        todo = Todo(task=task, user_id=user_id)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def update(todo, task=None, completed=None):
        if task:
            todo.task = task
        if completed is not None:
            todo.completed = completed
        db.session.commit()
        return todo

    @staticmethod
    def delete(todo):
        db.session.delete(todo)
        db.session.commit()