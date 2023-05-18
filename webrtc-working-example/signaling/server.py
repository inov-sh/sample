from aiohttp import web
import socketio

ROOM = 'room'
mcuID = '$'
latestPeer = '$'

sio = socketio.AsyncServer(cors_allowed_origins='*', ping_timeout=35)
app = web.Application()
sio.attach(app)


@sio.event
async def connect(sid, environ):
    global mcuID, latestPeer
    if mcuID == '$':
        mcuID = sid
    latestPeer = sid
    print('Connected', sid)
    await sio.emit('ready', room=sid)
    sio.enter_room(sid, ROOM)


@sio.event
def disconnect(sid):
    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)


@sio.event
async def data(sid, data):
    if (data['type'] == 'candidate' and sid != latestPeer and sid != mcuID):
        print('{}----{}-----{}'.format(sid, latestPeer, mcuID))
        return
    data['sid'] = sid
    print('Message from {}: {}'.format(sid, data['type']))
    await sio.emit('data', data, room=ROOM, skip_sid=sid)

@sio.event
async def receiver(sid, data):
    if (data['type'] == 'candidate' and sid != latestPeer and sid != mcuID):
        print('{}----{}-----{}'.format(sid, latestPeer, mcuID))
        return
    data['sid'] = sid
    print('Message from {}: {}'.format(sid, data['type']))
    await sio.emit('receiver', data, room=ROOM, skip_sid=sid)

if __name__ == '__main__':
    web.run_app(app, port=9999)
