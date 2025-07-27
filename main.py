import threading
import subprocess
from flask import Flask, request, jsonify
import yaml
import whisper_listener

app = Flask(__name__)

status = {
    'state': 'ready'
}

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


def listener_thread():
    global status
    status['state'] = 'listening'
    text = whisper_listener.listen(config)
    status['state'] = 'responding'
    if text:
        whisper_listener.handle_text(text, config)
    status['state'] = 'ready'


@app.route('/trigger', methods=['POST'])
def trigger():
    if status['state'] == 'ready':
        t = threading.Thread(target=listener_thread)
        t.start()
        return jsonify({'status': 'started'})
    else:
        return jsonify({'status': 'busy'}), 409


@app.route('/status')
def get_status():
    return jsonify(status)


if __name__ == '__main__':
    app.run(port=8723)
