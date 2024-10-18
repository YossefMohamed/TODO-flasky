from flask_restx import Resource, Namespace
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.todo_service import TodoService
from app.schemas.todo_schema import todo_schema, todos_schema

todos_ns = Namespace('todos', description='Todo operations')

@todos_ns.route('/')
class TodoList(Resource):
    @jwt_required()
    @todos_ns.doc(security='Bearer')
    def get(self):
        user_id = get_jwt_identity()
        todos = TodoService.get_all_todos(user_id)
        return todos_schema.dump(todos)

    @jwt_required()
    @todos_ns.expect(todo_schema)
    @todos_ns.doc(security='Bearer')
    def post(self):
        user_id = get_jwt_identity()
        data = request.json
        todo = TodoService.create_todo(data['task'], user_id)
        return todo_schema.dump(todo), 201

@todos_ns.route('/<int:todo_id>')
@todos_ns.doc(security='Bearer')
class Todo(Resource):
    @jwt_required()
    def get(self, todo_id):
        user_id = get_jwt_identity()
        todo = TodoService.get_todo(todo_id, user_id)
        if todo:
            return todo_schema.dump(todo)
        return {'message': 'Todo not found'}, 404

    @jwt_required()
    @todos_ns.expect(todo_schema)
    def put(self, todo_id):
        user_id = get_jwt_identity()
        data = request.json
        todo = TodoService.update_todo(todo_id, user_id, data.get('task'), data.get('completed'))
        if todo:
            return todo_schema.dump(todo)
        return {'message': 'Todo not found'}, 404

    @jwt_required()
    def delete(self, todo_id):
        user_id = get_jwt_identity()
        if TodoService.delete_todo(todo_id, user_id):
            return '', 204
        return {'message': 'Todo not found'}, 404

from app.api import api
api.add_namespace(todos_ns)