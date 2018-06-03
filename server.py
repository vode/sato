from flask import Flask, request, jsonify
import json
import requests
import os
import re
app = Flask(__name__)
port = int(os.environ["PORT"])
print(port)

mapper = {
  "比特币": "BTC",
  "火币平台币": "HT",
  "莱特币": "LTC",
  "以太币": "ETH",
}
crypto_list = [
"BTC",
"HT",
"LTC",
"ETH",
"XVG",
"EOS",
"XMR",
"比特币",
"火币平台币",
"莱特币",
"以太币",
"火币平台币",
"GRS",
"ETH",
"BTC",
"BCH",
"HT",
"QTUM",
"BQC",
"NCC",
"XRP",
"CAB",
"BQC",
"PHO",
"GPL",
"MND",
"NEO",
"XMR",
"WTC",
"ADA"
]

def format(name):
  if name in mapper:
    return mapper[name]
  else:
    return name
def match(name):
  pattern = re.compile(r'[a-zA-Z]*')
  match_result = re.search(pattern,name).group()
  return match_result

def get_name(data):
  try:
    for crypto in crypto_list:
      if crypto in data['nlp']['source']:
        return format(crypto)
    match_result = match(data['nlp']['source'])
    if match_result!= None and match_result != "":
      return match_result
    name = data['nlp']['entities']['crypto_name'][0]['raw']
    return format(name)
  except Exception:
    return ""


@app.route('/', methods=['POST'])
def index():
  print(port)
  
  data = json.loads(request.get_data())
  # FETCH THE CRYPTO NAME
  crypto_name = get_name(data)

  try:

    # FETCH BTC/USD/EUR PRICES
    r = requests.get("https://min-api.cryptocompare.com/data/price?fsym="+crypto_name+"&tsyms=BTC,USD,EUR")

    return jsonify(
      status=200,
      replies=[{
        'type': 'text',
        'content': '%s 的价格是 :\n%f BTC, \n%f USD, \n%f EUR.' % (crypto_name, r.json()['BTC'], r.json()['USD'], r.json()['EUR'])
      }]
    )
  except Exception:
    response_text = ""
    if crypto_name != "":
      response_text = "不好意思，小火查不到 %s 的行情呢" % (crypto_name)
    else:
      response_text = "不好意思，小火找不到您说的货币呢"
    return jsonify(
      status=200,
      replies=[{
        'type': 'text',
        'content': response_text
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
