import json

from flask import Flask
from flask import request, jsonify
import traceback
from controller.email_handler import EmailServiceHandler
from servicer.constants import Action


app = Flask(__name__)


@app.route('/email/action', methods=['POST'])
def execute_action():
    try:
        action = request.args.get('action')
        rules = request.files.get('rules')
        if not rules or not action:
            return jsonify({'error': 'data is missing'}), 400
        rules = json.loads(rules.stream.read())

        # todo this call can be async
        EmailServiceHandler().execute_email_actions(Action[action], rules)

        return jsonify({'message': 'Request processed successfully'}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/email/fetch', methods=['GET'])
def fetch_and_save_email():
    try:
        # todo this call can be async
        EmailServiceHandler().fetch_and_save_email()
        return jsonify({'message': 'Request processed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    try:
        return jsonify({'message': 'working'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

