"""dstr"""

import os
import time
import datetime

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pyotp
import robin_stocks.robinhood as r

class Bitcoin:
    def __init__(self):
        self.price = 0
        self.last_price = 0
        self.price_difference = 0

def get_bitcoin_price():
    """Get the current price of Bitcoin."""
    btc_qt = r.crypto.get_crypto_quote("BTC")
    return float(btc_qt['mark_price'])

# Create a function to update the graph.
def update_graph(i, x, y, coin):
    """Update the graph with the latest price."""
    coin.last_price = coin.price
    coin.price = get_bitcoin_price()
    x.append(i)
    y.append(coin.price)

    # Calculate the price difference with the last price.
    coin.price_difference = coin.price - coin.last_price
    f = open(file="prices.csv", mode="a", encoding="utf-8")
    f.write(f"{time.time()},{coin.price},{coin.price_difference}\n")
    f.close()

    ax.clear()
    ax.plot(x, y)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Bitcoin Price (USD)")
    ax.set_title("Real-time Bitcoin Price Graph")


#######################################################

try:
    totp  = pyotp.TOTP(os.environ.get("ROBINHOOD_TOTP")).now()
    login = r.login(mfa_code=totp)

    # Initialize an empty graph.
    x = []
    y = []

    fig, ax = plt.subplots()
    price = get_bitcoin_price()
    last_price = get_bitcoin_price()
    coin = Bitcoin()

    # Create an animation to update the graph every second.
    ani = FuncAnimation(fig, update_graph, fargs=(x, y, coin), interval=1000)
    plt.show()
except Exception as e:
    print(e)

# class EmergencyKill(Exception): ...

# plt.show()
# kill = False
# while True and not kill:
#     try:
#         last_price = price
#         price = get_bitcoin_price()
#         f.write(f"{time.time()},{price}\n")

#     # Calculate the price difference with the last price.
#         price_difference = price - last_price
#         print(f"Price Difference: {price_difference} USD")

#         time.sleep(.05)

#     except EmergencyKill: # Just in case
#         kill = True
#         print("Kill order sent " + str(datetime.datetime.utcnow()))
#         break
