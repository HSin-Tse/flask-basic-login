#!/usr/bin/env python
from threading import Lock
import urllib.parse
import requests
from flask import Flask, render_template, session, request, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
from contextlib import closing


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        # socketio.emit('my_response',
        #               {'data': 'Server generated event', 'count': count},
        #               namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@app.route('/<path:url>', methods=['GET', 'POST'])
def home(url):
    # emit('my_pong')

    session['receive_count'] = session.get('receive_count', 0) + 1

    # socketio.emit('my_response',
    #               {'data': request.url, 'count': session['receive_count']},
    #               namespace='/test')

    print(" request.url:", request.url, '-->File "runProxy.py", line 12')
    # a = ("http://stat.ajmide.com/stat" == request.url)
    # a = request.url.contain('stat.ajmide.com')
    # a = (request.url.indexOf("stat.ajmide.com") > 0)
    isstatic = ("stat.ajmide.com" in request.url)

    print(" request.method:", request.method, '-->File "runProxy.py", line 12')
    if (isstatic):
        print(" request.get_data():", request.get_data(), '-->File "runProxy.py", line 16')
        socketio.emit('my_response',
                      {'data': request.url, 'count': session['receive_count'],
                       'body': urllib.parse.unquote(str(request.get_data()), encoding="utf-8")},
                      namespace='/test')

        return ""

    with closing(

            requests.request(
                method=request.method,
                url=request.url,
                headers=request.headers,
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False)
    ) as resp:
        resp_headers = []
        for name, value in resp.headers.items():

            if name.lower() == 'connection':
                resp_headers.append((name, 'close'))

            if name.lower() in ('content-length', 'connection', 'content-encoding', 'transfer-encoding'):
                continue
            resp_headers.append((name, value))

        # excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        # headers = [(name, value) for (name, value) in resp.raw.headers.items()
        #            if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, resp_headers)

        return response


if __name__ == '__main__':
    # socketio.run(app, debug=True, port=5001)
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)
    # socketio.run(host="0.0.0.0", port=5001, debug=True, threaded=True)
