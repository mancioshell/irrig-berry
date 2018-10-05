from bson import ObjectId
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder): 
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)
