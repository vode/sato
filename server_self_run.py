from flask import Flask, request, jsonify
import json
import requests
import traceback
app = Flask(__name__)
port = '5001'

import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import requests

# 此处填写APIKEY

ACCESS_KEY = "d2e82710-03c51810-9fed7063-7ba8f"
SECRET_KEY = "b12fe6f4-dccb03b3-54fcdf43-bda24"



# API 请求地址
MARKET_URL = "https://api.huobi.pro"
TRADE_URL = "https://api.huobi.pro"

# 首次运行可通过get_accounts()获取acct_id,然后直接赋值,减少重复获取。
ACCOUNT_ID = None

#'Timestamp': '2017-06-02T06:13:49'

def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    response = requests.get(url, postdata, headers=headers, timeout=5) 
    try:
        
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpGet failed, detail is:%s,%s" %(response.text,e))
        return


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/json'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = json.dumps(params)
    response = requests.post(url, postdata, headers=headers, timeout=10)
    try:
        
        if response.status_code == 200:
            return response.json()
        else:
            return
    except BaseException as e:
        print("httpPost failed, detail is:%s,%s" %(response.text,e))
        return


def api_key_get(params, request_path):
    method = 'GET'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params.update({'AccessKeyId': ACCESS_KEY,
                   'SignatureMethod': 'HmacSHA256',
                   'SignatureVersion': '2',
                   'Timestamp': timestamp})

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params['Signature'] = createSign(params, method, host_name, request_path, SECRET_KEY)

    url = host_url + request_path
    return http_get_request(url, params)


def api_key_post(params, request_path):
    method = 'POST'
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    params_to_sign = {'AccessKeyId': ACCESS_KEY,
                      'SignatureMethod': 'HmacSHA256',
                      'SignatureVersion': '2',
                      'Timestamp': timestamp}

    host_url = TRADE_URL
    host_name = urllib.parse.urlparse(host_url).hostname
    host_name = host_name.lower()
    params_to_sign['Signature'] = createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
    url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
    return http_post_request(url, params)


def createSign(pParams, method, host_url, request_path, secret_key):
    sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
    encode_params = urllib.parse.urlencode(sorted_params)
    payload = [method, host_url, request_path, encode_params]
    payload = '\n'.join(payload)
    payload = payload.encode(encoding='UTF8')
    secret_key = secret_key.encode(encoding='UTF8')

    digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest)
    signature = signature.decode()
    return signature

# 获取merge ticker
def get_ticker(symbol):
    """
    :param symbol: 
    :return:
    """
    params = {'symbol': symbol}

    url = MARKET_URL + '/market/detail/merged'
    return http_get_request(url, params)

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
  print(name)
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
    for crypto in info_dic.keys():
      if crypto in data['nlp']['source'] or crypto.lower() in data['nlp']['source']:
        return format(crypto)
    for key in mapper.keys():
      if key in data['nlp']['source']:
        return mapper[key]
  except Exception:
    print(traceback.format_exc())
    return ""

def get_query(data):
  return data['nlp']['source']


def get_market_price(crypto_name):
  crypto_name = crypto_name.upper()
  response_txt = get_huobi_info(crypto_name)
  if response_text is None:
    response_text = gen_crypto_info(crypto_name)
  return response_text

def get_huobi_info(crypto_name):
  symbol = crypto_name.lower()+'usdt'
  ticker = get_ticker(symbol)
  try:
    price = ticker['tick']['ask'][0]
    high = ticker['tick']['high']
    low = ticker['tick']['low']
    amount = int(ticker['amount'])
    return ' 货币代号: %s\n 货币全称:%s\n 实时价格: %s$\n 今日最高价: %s$\n 今日最低价: %s$\n 来源交易所: %s' %(crypto_name,official_name,price,highday,lowday,'Huobi')
  except Exception:
    print(traceback.format_exc())
    return None
def gen_crypto_info(crypto_name):
  print(crypto_name)
  if is_crypto(crypto_name):
    try:
      r = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+crypto_name+"&tsyms=USD")
      print(r)
      price =  r.json()['DISPLAY'][crypto_name]["USD"]["PRICE"]
      openday = r.json()['DISPLAY'][crypto_name]["USD"]["OPENDAY"]
      highday = r.json()['DISPLAY'][crypto_name]["USD"]["HIGHDAY"]
      lowday = r.json()['DISPLAY'][crypto_name]["USD"]["LOWDAY"]
      market = r.json()['DISPLAY'][crypto_name]["USD"]["LASTMARKET"]
      change24 = r.json()['DISPLAY'][crypto_name]["USD"]["CHANGE24HOUR"]
      changeday = r.json()['DISPLAY'][crypto_name]["USD"]["CHANGEDAY"]
      official_name = get_official_name(crypto_name)
      return ' 货币代号: %s\n 货币全称:%s\n 实时价格: %s\n 今日最高价: %s\n 今日最低价: %s\n 24小时涨幅: %s\n 今日涨幅: %s\n 来源交易所: %s' %(crypto_name,official_name, price,highday,lowday,change24,changeday,market)
    except Exception:
      print(traceback.format_exc())
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
  data = json.loads(request.get_data(as_text=True))
  print(data)
  query = get_query(data)
  response_text = ""
  if("火币网" in query):
    response_text = "火币集团是全球领先的数字资产金融服务商。2013年，火币创始团队看到了区块链行业的巨大发展潜力，心怀推动全球新金融改革的愿景，创立火币集团。火币集团以“让金融更高效，让财富更自由”作为集团使命，秉承“用户至上”的服务理念，致力于为全球用户提供安全、专业、诚信、优质的服务。目前，火币集团已完成对新加坡、美国、日本、韩国、香港等多个国家及地区的布局。"
  elif(is_crypto(query)):
    query=get_name(data)
    response_text = get_market_price(query)
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
  
  data = json.loads(request.get_data(as_text=True))
  # FETCH THE CRYPTO NAME
  crypto_name = get_name(data)
  print(crypto_name)
  response_text = get_market_price(crypto_name)
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

@app.route('/',methods=['GET'])
def index():
  return jsonify(status=200,replies=[{'type':'text','content':'hello world'}])
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
app.debug=True
app.run(port=port,debug=True)
