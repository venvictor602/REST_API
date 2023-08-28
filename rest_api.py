from flask import Flask, request
from flask_restful import Api, Resource, reqparse,abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.app_context().push()

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"video(name = {name}, likes = {likes}, views = {views})"



#making a first resource 

# class Helloworld(Resource):

#     def get(self):
#         return {"data":"Hello world"}
#     def post(self):
#         return {"data":"postedd world"}


# api.add_resource(Helloworld, "/helloworld")


#passing specific data to the endpoint and supplying parameters

# class Helloworld(Resource):

#     def get(self, name, test):
#         return {"name":name, "test":test}
#     def post(self):
#         return {"data":"postedd world"}


#making some modifications 

# names = {
#     "tim":{"age":19, 'gender':"male"},
#     "bill":{"age":70, "gender":"male"}
# }

# class Helloworld(Resource):

#     def get(self, name):
#         return names[name]
#     def post(self):
#         return {"data":"postedd world"}


# api.add_resource(Helloworld, "/helloworld/<string:name>")


#----Creating somehting like a youtube ----

# video_put_args = reqparse.RequestParser() #this validate the fields you want to put in the endpoint and what it should accept
# video_put_args.add_argument("name", type = str, help = 'Name of the video is required', location = 'form', required = True) #adding the rquired true means that the field must not reeturn empty value 
# video_put_args.add_argument("views", type = int, help = 'Views of the video is required', location = 'form', required = True)
# video_put_args.add_argument("likes", type = int, help = 'likes of the video is required', location = 'form', required = True)


# videos = {}

# #making sure the program done crash if the video ID doesnt exist 

# def abort_if_id_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, message = "video Doesnt not exist based on the ID...")

# #checking if the video already exist
# def abort_if_video_exist(video_id):
#     if video_id  in videos:
#         abort(409, message = "Video already exist")



# class Video(Resource):
#     #this check and gets the available videos
#     def get(self, video_id):
#         abort_if_id_doesnt_exist(video_id) #this comes later when raising a error of deosnt exist 
#         return videos[video_id]

#     #this allows the creation of new videos
#     def put(self, video_id):
#         abort_if_video_exist(video_id)
#         args = video_put_args.parse_args()
#         videos[video_id] = args
#         return videos[video_id], 201 #201 stands for create 

#     def delete(self, video_id):
#         abort_if_id_doesnt_exist(video_id)
#         del videos[video_id]
#         return '', 204

# api.add_resource(Video, "/video/<int:video_id>")


#--------adding to a database ------------




video_put_args = reqparse.RequestParser() #this validate the fields you want to put in the endpoint and what it should accept
video_put_args.add_argument("name", type = str, help = 'Name of the video is required', location = 'form', required = True) #adding the rquired true means that the field must not reeturn empty value 
video_put_args.add_argument("views", type = int, help = 'Views of the video is required', location = 'form', required = True)
video_put_args.add_argument("likes", type = int, help = 'likes of the video is required', location = 'form', required = True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type = str, help = 'Name of the video is required', location = 'form') #adding the rquired true means that the field must not reeturn empty value 
video_update_args.add_argument("views", type = int, help = 'Views of the video is required', location = 'form')
video_update_args.add_argument("likes", type = int, help = 'likes of the video is required', location = 'form')



#resource field is way to define how an object will be serialized 

resource_field = {
    'id':fields.Integer,
    'name':fields.String,
    'views':fields.Integer,
    'likes':fields.Integer
}

class Video(Resource):
    #this check and gets the available videos
    @marshal_with(resource_field) #what this does is when we return take the return value and serialise it with that fields of resource_field
    #reason for doing this is because the result is an object so we need to serialize it 
    def get(self, video_id):
        result  = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = 'could not find video with that ID')
        return result

    #this allows the creation of new videos
    @marshal_with(resource_field)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result  = VideoModel.query.filter_by(id = video_id).first()
        if result:
            abort (409, message= "Video Id taken...")
        video = VideoModel(id = video_id, name =args['name'], views = args['views'], likes = args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201 #201 stands for create 

    @marshal_with(resource_field)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result  = VideoModel.query.filter_by(id = video_id).first()
        if not result:
            abort(404, message = "Video doesn't exit....")
        # this check for the field to modify or if the field returns non it wont modify it 
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()
        return result


    def delete(self, video_id):
        abort_if_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)