from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)
port = '5000'
app.run(port=port)

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
  "火币": "HT"
}
r = requests.get("https://www.cryptocompare.com/api/data/coinlist/")
info_dic = r.json()["Data"]

def is_crypto(name):
  if name in mapper or name in info_dic:
    return True
  else:
    return False


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
    for crypto in crypto_list.keys():
      if crypto in data['nlp']['source']:
        return format(crypto)
    for key in mapper:
      if key in data['nlp']['source']:
        return mapper[key]
  except Exception:
    return ""

def get_query(param):
  return data['nlp']['source']

def gen_crypto_info(crypto_name):
  if is_crypto(crypto_name):
    try:
      r = requests.get("https://min-api.cryptocompare.com/data/pricemultifull??fsym="+crypto_name+"&tsyms=USD")
      price =  r.json()['DISPLAY'][crypto_name]["USD"]["PRICE"]
      openday = r.json()['DISPLAY'][crypto_name]["USD"]["OPENDAY"]
      highday = r.json()['DISPLAY'][crypto_name]["USD"]["HIGHDAY"]
      lowday = r.json()['DISPLAY'][crypto_name]["USD"]["LOWDAY"]
      market = r.json()['DISPLAY'][crypto_name]["USD"]["LASTMARKET"]
      change24 = r.json()['DISPLAY'][crypto_name]["USD"]["CHANGEPCT24HOUR"]
      changeday = r.json()['DISPLAY'][crypto_name]["USD"]["CHANGEDAY"]
      official_name = get_official_name(crypto_name)
      return '货币代号: %s\n 货币全称:%s\n 实时价格: %s\n 今日最高价：%s\n 今日最低价: %s\n 24小时涨幅: %s\n 今日涨幅: %s\n 来源交易所: %s' 
            %(crypto_name,official_name, price,openday,highday,lowday,change24,changeday，market)
    except Exception:
      return "不好意思，小火查不到 %s 的行情呢" % (crypto_name)
  else:
    return "不好意思，小火找不到您说的数字货币呢"

def get_official_name(crypto_name):
  if crypto_name in info_dic:
    return info_dic[crypto_name]['FullName']
  else:
    return crypto_name


@app.route('/last', methods=['POST'])
def last():
  data = json.loads(request.get_data())
  query = get_query(data)
  response_text = ""
  if("火币网" in query):
    response_text = "火币集团是全球领先的数字资产金融服务商。2013年，火币创始团队看到了区块链行业的巨大发展潜力，心怀推动全球新金融改革的愿景，创立火币集团。火币集团以“让金融更高效，让财富更自由”作为集团使命，秉承“用户至上”的服务理念，致力于为全球用户提供安全、专业、诚信、优质的服务。目前，火币集团已完成对新加坡、美国、日本、韩国、香港等多个国家及地区的布局。"
  elif(is_crypto(query)):
    response_text = gen_crypto_info(query)
  else:
    response_text = "不好意思，小火不太明白你的问题呢\n你可以尝试提问：\n推荐群\n比特币的价格\n如何下载火币App\n火币网简介\n"
  return jsonify(
      status=200,
      replies=[{
        'type': 'text',
        'content': response_text
      }]
      )

@app.route('/price', methods=['POST'])
def price():
  print(port)
  
  data = json.loads(request.get_data())
  # FETCH THE CRYPTO NAME
  crypto_name = get_name(data)
  response_text = gen_crypto_info()
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
app.run(port=port)