from flask import Flask, render_template, session, copy_current_request_context
from flask_socketio import SocketIO, emit, disconnect
from threading import Lock
import socket as sk

# configure flask vars
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'robotics'
socket = SocketIO(app, async_mode=async_mode)
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
except ImportError as e:
    print(e)
    from mtrctrltest import Controller
controller = Controller(21)


"""
webroot returns index.html as template. Scripts/ccs need to be in static folder
and html needs needs to be in template folder. js need to be loaded in html
with this notation: 
<script src="{{url_for('static', filename='file_relative_to_static_folder.js')}}"></script>
css:
<link rel="stylesheet" href="{{ url_for('static', filename='file_relative_to_static_folder.css') }}" />
"""

@app.route('/')
def index():
    return render_template('indexcss.html',
                           sync_mode=socket.async_mode)


# need to update client with sensor/em status when connected
@socket.on('connect')
def connect():
    print('Client connected, updating data')
    socket.emit('response', {'update': {'em_on': controller.is_on}})


@socket.on('toggle_em')
def toggle_em(json):
    print('received my event: ' + str(json))
    if json['data']:
        controller.turn_on()
    else:
        controller.turn_off()

    socket.emit('response', {'update': {'em_on': controller.is_on}})


def toggle_em_cb(data):
    pass


"""
get local ipv4 to force flask to run on that address
needed bc flask requires a host ip for it to run
"""


def get_ip():
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    try:
        """socket hostnames on some linux systems return 127.0.0.1
        so try making connection and check socket """
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


if __name__ == '__main__':
    host_ip = get_ip()
    print('running on ip ' + host_ip+':5000')

    try:
        socket.run(app, debug=False, host=host_ip)
    # need to catch keyboard interrupt to clean up gpio
    # not sure if theres a better way to do this like an exit hook in python
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        print('exiting - cleaning up gpio')
        controller.cleanup()

"""
debug mode causes script to restart when run, 
don't be alarmed by multiple var outputs
*disable on production*
"""
