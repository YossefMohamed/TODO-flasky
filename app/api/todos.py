from flask_restx import Resource, Namespace, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.todo_service import TodoService
from app.schemas.todo_schema import todo_schema, todos_schema

todos_ns = Namespace('todos', description='Todo operations')

# Define model for Swagger UI
todo_model = todos_ns.model('Todo', {
    'task': fields.String(required=True, description='The task details'),
    'completed': fields.Boolean(description='Whether the task is completed')
})

@todos_ns.route('/')
class TodoList(Resource):
    @jwt_required()
    @todos_ns.doc(security='jwt')
    def get(self):
        user_id = get_jwt_identity()
        todos = TodoService.get_all_todos(user_id)
        return todos_schema.dump(todos)

    @jwt_required()
    @todos_ns.expect(todo_model)
    @todos_ns.doc(security='jwt')
    def post(self):
        user_id = get_jwt_identity()
        data = request.json
        todo = TodoService.create_todo(data['task'], user_id)
        return todo_schema.dump(todo), 201

@todos_ns.route('/<int:todo_id>')
class Todo(Resource):
    @jwt_required()
    @todos_ns.doc(security='jwt')
    def get(self, todo_id):
        user_id = get_jwt_identity()
        todo = TodoService.get_todo(todo_id, user_id)
        if todo:
            return todo_schema.dump(todo)
        return {'message': 'Todo not found'}, 404

    @jwt_required()
    @todos_ns.expect(todo_model)
    @todos_ns.doc(security='jwt')
    def put(self, todo_id):
        user_id = get_jwt_identity()
        data = request.json
        todo = TodoService.update_todo(todo_id, user_id, data.get('task'), data.get('completed'))
        if todo:
            return todo_schema.dump(todo)
        return {'message': 'Todo not found'}, 404

    @jwt_required()
    @todos_ns.doc(security='jwt')
    def delete(self, todo_id):
        user_id = get_jwt_identity()
        if TodoService.delete_todo(todo_id, user_id):
            return '', 204
        return {'message': 'Todo not found'}, 404

from app.api import api
api.add_namespace(todos_ns)