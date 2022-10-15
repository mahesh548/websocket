import express from 'express';

import { createServer } from 'https';
const port=8000
var app=express();
let server = createServer(app);
const io = require("socket.io")(server, {
    cors: {
      origin: "*",
      methods: ["GET", "POST"]
    }
  });
 
// make connection with user from server side
io.on('connection', (socket)=>{
  console.log('New user connected');
   //emit message from server to user
   socket.emit('newMessage', {
     from:'mahesh',
     text:'heyoo',
     createdAt:123
   });
 
  // listen for message from user
  socket.on('createMessage', (newMessage)=>{
    console.log('newMessage', newMessage);
  });

  socket.on('create', (newMessage)=>{
    console.log(newMessage)
    
  });
 
  // when server disconnects from user
  socket.on('disconnect', ()=>{
    console.log('disconnected from user');
  });
});
 
server.listen(port);