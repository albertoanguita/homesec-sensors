from http import HTTPStatus

from flask import Flask, request, jsonify

from api.dtos.StateDto import StateDto
from manager.Manager import Manager

app = Flask(__name__)  # Flask constructor
app.debug = True

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
def set_state():
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

@app.route('/test1', methods=['POST'])
def state2():
    input = request.json
    print(input)
    return jsonify(StateDto(state=State.RUNNING))

@app.route('/command', methods=['POST'])
def command():
    input = request.json
    command = input['command']
    arguments = input['arguments']
    manager.command(command, arguments)
    print(command)


if __name__ == '__main__':
    app.run(debug=True, port=5500)