"""Run the lab API with: python app.py."""
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import database

app = Flask(__name__)
CORS(app)
database.create_db_table()


def read_user(include_id=False):
    user = request.get_json()
    if not isinstance(user, dict):
        raise ValueError('The request body must be a JSON object.')
    for field in database.FIELDS:
        if not isinstance(user.get(field), str) or not user[field].strip():
            raise ValueError(f'{field} must be a non-empty string.')
    if include_id and (type(user.get('user_id')) is not int or user['user_id'] < 1):
        raise ValueError('user_id must be a positive integer.')
    return user


@app.errorhandler(ValueError)
def invalid_input(error):
    return jsonify(error=str(error)), 400


@app.errorhandler(HTTPException)
def http_error(error):
    return jsonify(error=error.description), error.code


@app.get('/api/users')
def api_get_users():
    return jsonify(database.get_users())


@app.get('/api/users/<int:user_id>')
def api_get_user(user_id):
    user = database.get_user_by_id(user_id)
    if user is None:
        return jsonify(error='User not found.'), 404
    return jsonify(user)


@app.post('/api/users/add')
def api_add_user():
    return jsonify(database.insert_user(read_user())), 201


@app.put('/api/users/update')
def api_update_user():
    user = database.update_user(read_user(include_id=True))
    if user is None:
        return jsonify(error='User not found.'), 404
    return jsonify(user)


@app.delete('/api/users/delete/<int:user_id>')
def api_delete_user(user_id):
    if not database.delete_user(user_id):
        return jsonify(error='User not found.'), 404
    return jsonify(status='User deleted successfully')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', '5001')))
