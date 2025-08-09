from http import HTTPStatus

from flask import Flask

from api.dtos.State import StateDto, AppState

app = Flask(__name__)  # Flask constructor


# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def hello():
    return 'HELLO'


@app.route('/state', methods=['GET'])
def state():
    return StateDto(state=AppState.RUNNING)


@app.route('/state', methods=['POST'])
def state(state: StateDto):
    return HTTPStatus.OK, state.state


if __name__ == '__main__':
    app.run(debug=True, port=5500)