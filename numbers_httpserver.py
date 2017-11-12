#!flask/bin/python
'''
This code creates the http server to play the numbers guessing game using REST API

Imports:
Flask to create http server and api
numbers to check if the particular instance is a number or not
'''
from flask import Flask, jsonify, abort, make_response, request
from numbers import Number

app = Flask(__name__)

range = None # range of values to choose from initially set to none
guesses = [] # guesses to be made


# get the value of range i.e., the minimum, and maximum values

@app.route('/range', methods = ['GET'])
def get_range():
    global range # For using the global variable locally and returning it.
    if range is None: 
        abort(404)
    # return json response of minimum and maximum values
    return jsonify({'minimum': range['minimum'], 'maximum': range['maximum']}), 200

# to post range (minimum, maximum and correct values)
@app.route('/range', methods=['POST'])
def post_range():
    global range, guesses # access the global variable append it locally
    guesses = [] # make guesses an empty list to start fresh for new values
    try:
        minimum = request.get_json()['minimum']
        maximum = request.get_json()['maximum']
        correct = request.get_json()['correct']
    except KeyError:
        abort(400)
    # check if minimum, maximum and correct values are numbers or not
    if not isinstance(minimum, Number) or not isinstance(maximum, Number) or not isinstance(correct, Number): 
        abort(400)
    if minimum >= maximum or correct < minimum or correct > maximum: 
        abort(400)
    # create range with mininum maximum and correct value chosen
    range = {'minimum': minimum, 'maximum': maximum, 'correct': correct}
    return jsonify(range), 201 # return max min and correct values chosen as response to the client

# returns a history of guesses made until now
@app.route('/guesses', methods=['GET'])
def get_guesses():
    global guesses
    return jsonify({'guesses': guesses}), 200# json dictionary that is returned

# post the values to guess the correct value chosen in the range (actual game logic) 
@app.route('/guesses', methods=['POST'])
def post_guesses():
    global range, guesses # use global variables to access and modify them locally
    # handling bad requests
    if range is None: 
        abort(400)
    if not request.get_json() or not 'guess' in request.get_json(): 
        abort(400)

    guess = request.get_json()['guess']# storing the value of guess from the user
    # check if the guess is not a number
    if not isinstance(request.get_json()['guess'], Number): 
        abort(400)

    result = None # variable to store the result of comparing guess value to true value
    if guess < range['minimum'] or guess > range['maximum']: 
        result = 'outside range'
    elif guess == range['correct']: 
        result = 'correct'
    elif guess > range['correct']: 
        result = 'higher than correct value'
    elif guess < range['correct']: 
        result = 'lower than correct value'

    guessResult = {'guess': guess, 'result': result}# store the result of a particular guess in a dict
    guesses.append(guessResult)# append it to the guesses to get history of guesses
    return jsonify(guessResult), 201 # return json object of the computation


# error handling in case of resource not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
# error handling for bad requests
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

if __name__ == '__main__':
    app.run(debug=True)

