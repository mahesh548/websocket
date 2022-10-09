from socket import socket
from flask import Flask, render_template,request
from flask_socketio import SocketIO,join_room,send,leave_room,emit
from flask_cors import CORS,cross_origin
import requests
import json
app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
},methods=["POST","GET"])
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


USERS={}
VIDEOCALL={}
@socketio.on('create')

def create(data):
    username = data['username']
    room = data['room']
    print(room)
    join_room(room)
    head={"Authorization":"Bearer d59ea031470c7298d7d3c389b3757dc87ca91769cc4db45c6359650ae8961ccd"}
    mkm={"name": room,
       "privacy": "private",
       
       "properties" : {
          "start_audio_off":False,
          "start_video_off":False
        }
        }
    r=requests.post("https://api.daily.co/v1/rooms/",headers=head,data=json.dumps(mkm))
    mkm2={
        "properties" :{
            "room_name":room
        }
        
    }
    r=requests.post("https://api.daily.co/v1/meeting-tokens",headers=head,data=json.dumps(mkm2))
    VIDEOCALL[room]=r.json()['token']
    USERS[request.sid]={"room":room,"username":username,"post":"player"}
    emit("crate_success",username + ' Your Room Created, ROOM: ' +room, room=room)


@socketio.on('join')

def on_join(data):
    username = data['username']
    room = data['room']
    print(room)
    join_room(room)
    USERS[request.sid]={"room":room,"username":username,"post":"listener"}
    mkm={
        "username":username,
        "id":request.sid
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
        "subtitle":data["subtitle"],
        "paused":data["paused"],
        "members":data["members"]
    }
    emit("room_updated",mkm, room=room)



@socketio.on('sync')

def sync(data):
    room = data['room']
    emit("sync", room=room)



@socketio.on("con")

def j(data):
    room=data["room"]
    user=data["user"]
    join_room(room)
    USERS[request.sid]={"room":room,"username":user}
    print(user+" joined the room "+room)


@socketio.on('disconnect')

def disconnect():
    sid = request.sid
    if(USERS[sid]["post"]=="listener"):
        mkm={
        "username":USERS[sid]["username"],
        "id":sid
        }
        emit("user_leave",mkm,room=USERS[request.sid]["room"])
    if (USERS[sid]["post"]=="player"):
        head={"Authorization":"Bearer d59ea031470c7298d7d3c389b3757dc87ca91769cc4db45c6359650ae8961ccd"}
        room=USERS[request.sid]["room"]
        r=requests.delete("https://api.daily.co/v1/rooms/"+room,headers=head)
        emit("player_leave",room=USERS[request.sid]["room"])


@socketio.on('videocall')

def videocall(data):
    room=data["room"]

    mkm={
        "token":VIDEOCALL[room]
    }
    emit("token",mkm,room=request.sid)




if __name__ == '__main__':
    #app.run()
    socketio.run(app,host="localhost",port=8000)




