from marshmallow import Schema, fields

class TodoSchema(Schema):
    id = fields.Int(dump_only=True)
    task = fields.Str(required=True)
    completed = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)