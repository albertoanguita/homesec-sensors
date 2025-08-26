import os
from http import HTTPStatus

from flask import Flask, request, jsonify

from api.dtos.StateDto import StateDto
from manager.Manager import Manager

app = Flask(__name__)  # Flask constructor
app.debug = True

# set cwd to base project dir
os.chdir('C:/Users/alber/repos/homesec-sensors')

manager = Manager()

# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def hello():
    return 'HELLO'


@app.route('/homesec-sensors/state', methods=['GET'])
def get_state():
    state = manager.get_state().name
    stateDto = StateDto(state)
    return jsonify(stateDto)


@app.route('/homesec-sensors/command', methods=['POST'])
def command():
    input = request.json
    if input is None or not 'command' in input:
        return "Invalid input state", HTTPStatus.BAD_REQUEST
    value = input['command']
    if value is None:
        return "Invalid input state", HTTPStatus.BAD_REQUEST

    if manager.command(value):
        return jsonify(success=True)
    else:
        return "Invalid input state", HTTPStatus.BAD_REQUEST


@app.route('/set-callback-url', methods=['POST'])
def set_callback_url():
    input = request.json
    if input is None or not 'url' in input:
        return "Invalid body", HTTPStatus.BAD_REQUEST
    value = input['url']
    if value is None:
        return "Invalid body", HTTPStatus.BAD_REQUEST

    manager.set_callback_url(value)
    return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True, port=5500)