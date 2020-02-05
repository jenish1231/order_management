from flask_restful import Resource, abort


class CreateListResource(Resource):
    def __init__(self):
        super().__init__()
        assert hasattr(self, 'model'), "Must include model"
        assert hasattr(self, 'schema'), "Must include a schema"

        self.name = self.model.__name__.lower() + 's'

    def get(self):
        object_list = self.model.query.all()
        result = self.schema(many=True).dump(object_list)
        return { self.name : result }

    def post(self):
        json_data = request.get_json()

        try:
            data = self.schema().load(json_data)
        except ValidationError as err:
            return err.messages, 400
        
        obj = self.model(**data)
        db.session.add(obj)
        db.session.commit()
        return data

class DetailUpdateDeleteResource(Resource):
    def __init__(self):
        super().__init__()
        
        assert hasattr(self, 'model'), "Must include model"
        assert hasattr(self, 'schema'), "Must include a schema"

        self.name = self.model.__name__
        

    def get_object(self, id):
        try:
            int(id)
        except:
            return {"message" : "Invalid parameters"}
        obj = self.model.query.get(id)
        if not obj:
            abort(404, message="{} {} doesnot exist".format(self.name, id))
        return obj


    def get(self, id):
        obj = self.get_object(id)
        
        obj_result = self.schema().dump(obj)
        return obj_result

    def delete(self, id):
        obj = self.get_object(id)
        db.session.delete(obj)
        db.session.commit()
        return '', 204

    def put(self, id):
        obj = self.get_object(id)
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