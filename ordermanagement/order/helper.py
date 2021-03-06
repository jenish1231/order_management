from flask_restful import Resource, abort
from flask import request
from marshmallow import ValidationError
from .models import db

class BaseResource(Resource):
    def __init__(self):
        super().__init__()
        assert hasattr(self, 'model'), "Must include model"
        assert hasattr(self, 'schema'), "Must include a schema"

# class GetObject(object):
#     def __init__(self):
#         super().__init__()
#         self.name = self.model.__name__.lower() + 's'

#     def get_object(self, id):
#         try:
#             int(id)
#         except:
#             return {"message" : "Invalid parameters"}
        
#         obj = self.model.query.get(id)
#         if not obj:
#             abort(404, message="{} {} doesnot exist".format(self.name, id))
#         return obj

def get_object_or_404(Klass, id):
    try:
        int(id)
    except:
        return {"message" : "Invalid parameters"}
    
    obj = Klass.query.get(id)
    if not obj:
        abort(404, message="{} {} doesnot exist".format(Klass.__name__, id))
    return obj
    
class CreateResource(BaseResource):
    def post(self):
        json_data = request.get_json()

        try:
            data = self.schema().load(json_data)
        except ValidationError as err:
            return err.messages, 400
        
        self.obj = self.model(**data)

        self.obj.save()
        return self.schema().dump(self.obj), 200

class DetailResource(BaseResource):
    
    def get(self, id):
        obj = get_object_or_404(self.model, id)
        if not isinstance(obj, self.model):
            return obj
        
        obj_result = self.schema().dump(obj)
        return obj_result

class ListResource(BaseResource):
    def __init__(self):
        super().__init__()
        self.name = self.model.__name__.lower() + 's'
        

    def get(self):
        object_list = self.model.query.all()
        result = self.schema(many=True).dump(object_list)
        return { self.name : result }

class UpdateResource(BaseResource):

    def put(self, id):
        obj = get_object_or_404(self.model, id)

        if not isinstance(obj, self.model):
            return obj

        json_data = request.get_json()

        try:
            data = self.schema().load(json_data)
        except ValidationError as err:
            return err.messages, 400
        
        for field in self.model.__table__.columns:
            field_name = vars(field)['name']
            if field_name in data.keys():
                setattr(obj, field_name, data[field_name])
        db.session.commit()
        return self.schema().dump(obj)

class DeleteResource(BaseResource):

    def delete(self, id):
        obj = get_object_or_404(self.model, id)
        obj.delete()
        return '', 204

