import os
import yaml
from flask import Flask, Blueprint, request, jsonify, render_template


def load_config():
    if os.path.exists('hub_config.yaml'):
        with open('hub_config.yaml') as f:
            return yaml.safe_load(f)
    return {}


def create_app(with_ui=False, persistent=False, with_comm=False):
    app = Flask(__name__)
    config = load_config()
    storage_file = config.get('storage_file', 'hub_data.yaml')

    data = {'agents': {}, 'tasks': [], 'wiki': {}, 'messages': []}
    if persistent and os.path.exists(storage_file):
        with open(storage_file) as f:
            loaded = yaml.safe_load(f) or {}
            for key in data:
                if key in loaded:
                    data[key] = loaded[key]

    def save():
        if persistent:
            with open(storage_file, 'w') as f:
                yaml.safe_dump(data, f)

    register_bp = Blueprint('register', __name__)

    @register_bp.route('/register', methods=['POST'])
    def register():
        info = request.json or {}
        agent_id = info.get('id')
        if not agent_id:
            return jsonify({'error': 'id required'}), 400
        data['agents'][agent_id] = {
            'role': info.get('role', ''),
            'profile': info.get('profile', '')
        }
        save()
        return jsonify({'status': 'registered'})

    tasks_bp = Blueprint('tasks', __name__)

    @tasks_bp.route('/tasks', methods=['GET', 'POST', 'PUT'])
    def tasks():
        if request.method == 'GET':
            return jsonify(data['tasks'])
        entry = request.json or {}
        if request.method == 'POST':
            data['tasks'].append(entry)
        else:  # PUT
            tid = entry.get('id')
            for i, t in enumerate(data['tasks']):
                if t.get('id') == tid:
                    data['tasks'][i] = entry
                    break
        save()
        return jsonify({'status': 'ok'})

    wiki_bp = Blueprint('wiki', __name__)

    @wiki_bp.route('/wiki/<name>', methods=['GET', 'POST'])
    def wiki(name):
        if request.method == 'GET':
            return jsonify({'name': name, 'content': data['wiki'].get(name, '')})
        if request.is_json:
            text = request.json.get('content', '')
        else:
            text = request.data.decode()
        data['wiki'][name] = text
        save()
        return jsonify({'status': 'saved'})

    status_bp = Blueprint('status', __name__)

    @status_bp.route('/status')
    def status():
        return jsonify({
            'agents': list(data['agents'].keys()),
            'task_count': len(data['tasks']),
            'wiki_entries': len(data['wiki']),
            'messages': len(data['messages'])
        })

    app.register_blueprint(register_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(wiki_bp)
    app.register_blueprint(status_bp)

    if with_comm:
        messages_bp = Blueprint('messages', __name__)

        @messages_bp.route('/message', methods=['POST', 'GET'])
        def message():
            if request.method == 'POST':
                entry = request.json or {}
                data['messages'].append(entry)
                save()
                return jsonify({'status': 'sent'})
            agent = request.args.get('agent')
            msgs = [m for m in data['messages'] if m.get('to') == agent]
            return jsonify(msgs)

        app.register_blueprint(messages_bp)

    if with_ui:
        dashboard_bp = Blueprint('dashboard', __name__)

        @dashboard_bp.route('/dashboard')
        def dashboard():
            return render_template('dashboard.html', data=data)

        app.register_blueprint(dashboard_bp)

    return app
