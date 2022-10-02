from flask import Flask, render_template
from flask_socketio import SocketIO,join_room,send,leave_room,emit
from flask_cors import CORS,cross_origin
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
},methods=["POST","GET"])
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")



@socketio.on('create')

def create(data):
    username = data['username']
    room = data['room']
    print(room)
    join_room(room)
    emit("crate_success",username + ' Your Room Created, ROOM: ' +room, room=room)


@socketio.on('join')

def on_join(data):
    username = data['username']
    room = data['room']
    print(room)
    join_room(room)
    mkm={
        "user":username
    }
    emit("user_joined",mkm, room=room)

@socketio.on('leave')

def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    emit("room_message",username + ' has left the room.', room=room)


@socketio.on('update_room')

def update_room(data):
    username = data['username']
    room = data['room']
    mkm={
        "url":data["url"],
        "dura":data["duration"],
        "thumbnail":data["thumbnail"],
        "title":data["title"],
        "subtitle":data["subtitle"]
    }
    emit("room_updated",mkm, room=room)



@socketio.on('sync')

def sync(data):
    room = data['room']
    emit("sync", room=room)

if __name__ == '__main__':
    app.run()