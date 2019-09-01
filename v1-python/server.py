import os
from flask import Flask, request, jsonify
from Blockchain import Blockchain
import json

def create_app(test_config=None):


    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    blockchain = Blockchain()

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    @app.route('/nodes/register', methods=['POST'])
    def register_nodes():
        values = request.get_json()

        nodes = values.get('nodes')
        if nodes is None:
            return "Error: Supply a valid list of nodes", 400

        for node in nodes:
            blockchain.add_node(node)
        
        response = {
            "message": "New nodes have been added",
            "total_nodes": list(blockchain.nodes)
        }
        return jsonify(response), 201


    return app