from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock

# configure flask vars
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'robotics'
socket_ = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

# configure motor controller
"""
check if computer contains RPi.GPIO module
RPi.GPIO is only avaliable on pi so if import fails it will default to the testing module
which just stores bool for on or not for testing.
"""
try:
    from mtrctrl import Controller
except ImportError:
    from mtrctrltest import Controller
controller = Controller(21)

@app.route('/')
def index():
    return render_template('index.html',
                           sync_mode=socket_.async_mode)


@socket_.on('toggle_em', namespace='/controls')
def test_message():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'I GOT YOUR MESSAGE', 'count': session['receive_count']})


if __name__ == '__main__':
    socket_.run(app, debug=True)
"""
debug mode causes script to restart when run, 
don't be alarmed by multiple var outputs
*disable on production*
"""