import requests
from flask import Flask, jsonify

app = Flask(_name_)

# Configuration
WINDOW_SIZE = 10
THIRD_PARTY_API_URLS = {
    'p': "http://20.244.56.144/test/primes",
    'f': "http://20.244.56.144/test/fibo",
    'e': "http://20.244.56.144/test/even",
    'r': "http://20.244.56.144/test/rand"
}


stored_numbers = []


def fetch_numbers(number_type):
    response = requests.get(THIRD_PARTY_API_URLS[number_type])
    if response.status_code == 200:
        return response.json().get('numbers', [])
    else:
        return None


def calculate_average(numbers):
    if len(numbers) == 0:
        return None
    return sum(numbers) / len(numbers)


@app.route('/numbers/<number_type>')
def process_request(number_type):
    global stored_numbers
    numbers = fetch_numbers(number_type)

    if numbers is None:
        return jsonify({"error": "Unable to fetch numbers from third-party server"}), 500

    stored_numbers = list(set(stored_numbers + numbers))

    if len(stored_numbers) > WINDOW_SIZE:
        stored_numbers = stored_numbers[-WINDOW_SIZE:]

    avg = calculate_average(stored_numbers[-WINDOW_SIZE:])

    response = {
        "windowPrevState": stored_numbers[:-len(numbers)],
        "windowCurrState": stored_numbers[-len(numbers):],
        "numbers": numbers,
        "avg": avg
    }

    return jsonify(response), 200


if _name_ == '_main_':
    app.run(port=9876)