import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')


sio.connect('http://localhost:3000')
sio.wait()