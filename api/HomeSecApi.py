from http import HTTPStatus

from flask import Flask, request, jsonify

from api.dtos.State import StateDto, State

app = Flask(__name__)  # Flask constructor
app.debug = True


# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def hello():
    return 'HELLO'


@app.route('/state', methods=['GET'])
def state():
    return StateDto(state=State.RUNNING)


@app.route('/state', methods=['POST'])
def state1():
    return HTTPStatus.OK, state.state

@app.route('/test1', methods=['POST'])
def state2():
    input = request.json
    print(input)
    return jsonify(StateDto(state=State.RUNNING))


if __name__ == '__main__':
    app.run(debug=True, port=5500)