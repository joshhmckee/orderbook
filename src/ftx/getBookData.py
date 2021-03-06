import websocket
import json
import threading
import time

# Collect FTX coin data using a websocket connection

def on_open(ws):
    print("Opened")

    # Send channel and market subscribe msg to websocket
    msg = json.dumps({'op': 'subscribe', 'channel': 'orderbook', 'market': 'APE-PERP'})
    ws.send(msg)

bid = []
ask = []
best_bids = []
best_asks = []
times = []

def on_message(ws, message):
    global bid, ask
    global best_bids, best_asks, times
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
    
    best_bids.append(bid[0][0])
    best_asks.append(ask[0][0])
    times.append(time.time())

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed")

# Setup websocket to run as background thread: https://stackoverflow.com/questions/65656221/binance-websocket-realtime-plot-without-blocking-code?rq=1
def wsthread(best_bid, best_ask, times):
    ws = websocket.WebSocketApp("wss://ftx.com/ws/",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    ws.run_forever()

t = threading.Thread(target=wsthread, args=(best_bids, best_asks, times)) #args are the vars to get access to outside the websocket
t.start()



import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('dark_background')
fig, ax = plt.subplots()

def animate(i):
  ax.clear()
  refreshLength = -3000
  ax.plot(times[refreshLength:], best_bids[refreshLength:])
  ax.plot(times[refreshLength:], best_asks[refreshLength:])

anim = FuncAnimation(fig, animate, interval=10)

plt.show()