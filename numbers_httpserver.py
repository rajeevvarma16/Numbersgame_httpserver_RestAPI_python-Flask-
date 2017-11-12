#!flask/bin/python
'''
This code creates the http server
to play the numbers guessing game using REST API

Imports:
Flask to create http server and api
numbers to check if the particular instance is a number or not
'''
from flask import Flask, jsonify, abort, make_response, request
from numbers import Number

app = Flask(__name__)
range = None
guesses = []


@app.route('/range', methods = ['GET'])
def get_range():
    global range
    if range is None:
        abort(404)
    return jsonify({'minimum': range['minimum'], 'maximum': range['maximum']}), 200


@app.route('/range', methods=['POST'])
def post_range():
    global range, guesses
    guesses = []
    try:
        minimum = request.get_json()['minimum']
        maximum = request.get_json()['maximum']
        correct = request.get_json()['correct']
    except KeyError:
        abort(400)
    if not isinstance(minimum, Number) or not isinstance(maximum, Number) or not isinstance(correct, Number):
        abort(400)
    if minimum >= maximum or correct < minimum or correct > maximum:
        abort(400)
    range = {'minimum': minimum, 'maximum': maximum, 'correct': correct}
    return jsonify(range), 201


@app.route('/guesses', methods=['GET'])
def get_guesses():
    global guesses
    return jsonify({'guesses': guesses}), 200


@app.route('/guesses', methods=['POST'])
def post_guesses():
    global range, guesses
    if range is None:
        abort(400)
    if not request.get_json() or 'guess' not in request.get_json():
        abort(400)

    guess = request.get_json()['guess']

    if not isinstance(request.get_json()['guess'], Number):
        abort(400)

    result = None
    if guess < range['minimum'] or guess > range['maximum']:
        result = 'outside range'
    elif guess == range['correct']:
        result = 'correct'
    elif guess > range['correct']:
        result = 'higher than correct value'
    elif guess < range['correct']:
        result = 'lower than correct value'

    guessResult = {'guess': guess, 'result': result}
    guesses.append(guessResult)
    return jsonify(guessResult), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
