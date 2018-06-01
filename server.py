from flask import Flask, request, jsonify
import json
import requests
import os

app = Flask(__name__)
port = int(os.environ["PORT"])
print(port)

@app.route('/', methods=['POST'])
def index():
  print(port)
  data = json.loads(request.get_data())
  # FETCH THE CRYPTO NAME
  crypto_name = data['nlp']['entities']['crypto_name']['raw']
  try:
    # FETCH THE CRYPTO NAME
    crypto_name = data['nlp']['entities']['crypto_name']['raw']

    # FETCH BTC/USD/EUR PRICES
    r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+crypto_name+"&tsyms=BTC,USD,EUR")

    return jsonify(
      status=200,
      replies=[{
        'type': 'text',
        'content': '%s 的价格是 :\n%f BTC, \n%f USD, and \n%f EUR.' % (crypto_name, r.json()['BTC'], r.json()['USD'], r.json()['EUR'])
      }]
    )
  except Exception:
    return jsonify(
      status=200,
      replies=[{
        'type': 'text',
        'content': "不好意思，小火查不到 %s 的行情呢" % (crypto_name)
      }]
    )

@app.route('/test', methods=['POST'])
def test():
  print(port)
  data = json.loads(request.get_data())

  # FETCH THE CRYPTO NAME
  crypto_name = "BTC"

  # FETCH BTC/USD/EUR PRICES
  r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+crypto_name+"&tsyms=BTC,USD,EUR")

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': '%s 的价格是 %s is :\n%f BTC, \n%f USD, and \n%f EUR.' % (crypto_name, r.json()['BTC'], r.json()['USD'], r.json()['EUR'])
    }]
  )

@app.route('/test_view', methods=['GET'])
def test_view():
  
  # FETCH THE CRYPTO NAME
  crypto_name = "BTC"

  # FETCH BTC/USD/EUR PRICES
  r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+crypto_name+"&tsyms=BTC,USD,EUR")

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': '%s 的价格是 %s is :\n%f BTC, \n%f USD, and \n%f EUR.' % (crypto_name, r.json()['BTC'], r.json()['USD'], r.json()['EUR'])
    }]
  )

@app.route('/view', methods=['POST'])
def view():
  print(port)
  data = json.loads(request.get_data())

  # FETCH THE CRYPTO NAME
  crypto_name = "BTC"

  # FETCH BTC/USD/EUR PRICES
  r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+crypto_name+"&tsyms=BTC,USD,EUR")

  return jsonify(
    status=200,
    replies=[{
      'type': 'text',
      'content': json.dumps(data)
    }]
  )

@app.route('/errors', methods=['POST'])
def errors():
  print(json.loads(request.get_data()))
  return jsonify(status=200)

app.run(port=port, host="0.0.0.0")
