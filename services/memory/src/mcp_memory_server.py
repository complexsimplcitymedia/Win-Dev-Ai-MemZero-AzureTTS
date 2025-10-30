from flask import Flask, request, jsonify
from src.config.mcp_settings import MEMORY_SERVER_HOST, MEMORY_SERVER_PORT
import requests

app = Flask(__name__)

memory_store = {}

@app.route('/memory', methods=['POST'])
def store_memory():
    data = request.json
    key = data.get('key')
    value = data.get('value')
    if key and value:
        memory_store[key] = value
        return jsonify({'message': 'Memory stored successfully'}), 200
    return jsonify({'error': 'Invalid data'}), 400

@app.route('/memory/<key>', methods=['GET'])
def retrieve_memory(key):
    value = memory_store.get(key)
    if value:
        return jsonify({'key': key, 'value': value}), 200
    return jsonify({'error': 'Memory not found'}), 404

@app.route('/memory/<key>', methods=['DELETE'])
def delete_memory(key):
    if key in memory_store:
        del memory_store[key]
        return jsonify({'message': 'Memory deleted successfully'}), 200
    return jsonify({'error': 'Memory not found'}), 404

@app.route('/memory/jobs', methods=['GET'])
def get_all_jobs():
    jobs = {key: value for key, value in memory_store.items() if key.startswith('job_')}
    return jsonify({'jobs': jobs}), 200

if __name__ == '__main__':
    app.run(host=MEMORY_SERVER_HOST, port=MEMORY_SERVER_PORT)
