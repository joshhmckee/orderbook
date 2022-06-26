import websocket
import json
import time
import pandas as pd
from IPython.display import display

orderbook = []
bid = []
ask = []

def on_message(ws, message):
    global orderbook
    global bid
    global ask
    # Format orderbook message and store updata data in a dict
    msg = json.loads(message)
    if msg['type'] == 'partial':
      data = msg['data']
      bid = data['bids']
      ask = data['asks']
    elif msg['type'] == 'update':
      data = msg['data']
      update_bid = data['bids']
      update_ask = data['asks']
      for neworder in update_bid:
        if float(neworder[1]) == 0:
          for (i, order) in enumerate(bid):
            if neworder[0] == order[0]:
              bid.pop(i)
              break
        else:
          for i, order in enumerate(bid):
            if neworder[0] > order[0]:
              bid.insert(i, neworder)
              break
            elif neworder[0] == order[0]:
              bid[i] = neworder
              break
            elif i == len(bid) - 1:
              bid.append(neworder)
              break
      for neworder in update_ask:
        if float(neworder[1]) == 0:
          for (i, order) in enumerate(ask):
            if neworder[0] == order[0]:
              ask.pop(i)
              break
        else:
          for (i, order) in enumerate(ask):
            if neworder[0] < order[0]:
              ask.insert(i, neworder)
              break
            elif neworder[0] == order[0]:
              ask[i] = neworder
              break
            elif i == len(ask) - 1:
              ask.append(neworder)
              break
    print(bid[:3])
    #bids = pd.DataFrame(bid, columns = ['Bid', "Bidsize"])
    #asks = pd.DataFrame(ask, columns = ['Ask', "Asksize"])
    #orderbook = pd.concat([bids, asks], axis = 1)
    #orderbook = orderbook[['Bidsize', 'Bid', 'Ask', 'Asksize']]
    #display(orderbook)


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Connecting to FTX")
    request = json.dumps({'op': 'subscribe', 'channel': 'orderbook', 'market': 'BTC-PERP'})
    ws.send(request)


ws = websocket.WebSocketApp("wss://ftx.com/ws/",
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
ws.run_forever()