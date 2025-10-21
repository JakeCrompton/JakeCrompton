import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import random
from datetime import datetime, timedelta
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button

# === CONFIGURATION ===
TIME_FRAME_SECONDS = 1
INITIAL_PRICE = 2000.0
VOLATILITY = 0.5
START_BALANCE = 100000.0

# === TRADING STATE ===
balance = START_BALANCE
holdings = 0.0
avg_buy_price = 0.0
lot_size = 1
last_action = "None"

# === MARKET STATE ===
ohlc_data = []
candle_start = datetime.now()
current_open = INITIAL_PRICE
current_high = INITIAL_PRICE
current_low = INITIAL_PRICE
current_close = INITIAL_PRICE

# === PLOT SETUP ===
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)
plt.title("Gold Trading Simulation")

# === FAIR VALUE GAPS ===
fvg_zones = []

def generate_price(last_price):
    return round(last_price + random.uniform(-VOLATILITY, VOLATILITY), 2)

def buy(event=None):
    global balance, holdings, avg_buy_price, last_action
    cost = current_close * lot_size
    if balance >= cost:
        new_holdings = lot_size
        total_cost = cost
        new_total_holdings = holdings + new_holdings

        if holdings == 0:
            avg_buy_price = current_close
        else:
            avg_buy_price = ((avg_buy_price * holdings) + (current_close * new_holdings)) / new_total_holdings

        holdings = new_total_holdings
        balance -= total_cost
        last_action = f"Bought {lot_size} @ {current_close:.2f}"
    else:
        last_action = "Not enough balance to buy"

def sell(event=None):
    global balance, holdings, avg_buy_price, last_action
    if holdings > 0:
        value = holdings * current_close
        balance += value
        last_action = f"Sold {holdings:.2f} @ {current_close:.2f} = £{value:.2f}"
        holdings = 0
        avg_buy_price = 0
    else:
        last_action = "Nothing to sell"

def on_key(event):
    global lot_size
    if event.key == '1':
        lot_size = 1
    elif event.key == '2':
        lot_size = 2
    elif event.key == '5':
        lot_size = 5
    elif event.key == '0':
        lot_size = 10

def update(frame):
    global current_open, current_high, current_low, current_close, candle_start

    now = datetime.now()
    new_price = generate_price(current_close)
    current_close = new_price
    current_high = max(current_high, new_price)
    current_low = min(current_low, new_price)

    if now >= candle_start + timedelta(seconds=TIME_FRAME_SECONDS):
        ohlc_data.append([
            mdates.date2num(candle_start),
            current_open,
            current_high,
            current_low,
            current_close
        ])

        # Check for FVG (simplified logic: candle opens above previous high)
        if len(ohlc_data) >= 2:
            prev = ohlc_data[-2]
            curr = ohlc_data[-1]
            if curr[1] > prev[2]:  # current open > previous high
                fvg_zones.append((prev[2], curr[1]))

        candle_start = now
        current_open = new_price
        current_high = new_price
        current_low = new_price
        current_close = new_price

        if len(ohlc_data) > 60:
            ohlc_data.pop(0)

    # Plotting
    ax.clear()
    ax.set_title("Gold Trading Simulation")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.grid(True)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    if ohlc_data:
        df = pd.DataFrame(ohlc_data, columns=['Date', 'Open', 'High', 'Low', 'Close'])
        width = 1 / (24 * 60 * 60) * TIME_FRAME_SECONDS * 0.7

        for i in range(len(df)):
            date = df['Date'][i]
            open_ = df['Open'][i]
            high = df['High'][i]
            low = df['Low'][i]
            close = df['Close'][i]

            color = 'green' if close >= open_ else 'red'
            lower = min(open_, close)
            height = max(abs(close - open_), 0.01)

            ax.vlines(date, low, high, color='black', linewidth=1)
            ax.bar(date, height, width=width, bottom=lower, color=color, align='center')

        # Plot fair value gaps
        for low, high in fvg_zones[-10:]:  # only show recent gaps
            ax.axhspan(low, high, color='yellow', alpha=0.3)

        ax.set_xlim(df['Date'].min() - width, df['Date'].max() + width)
        ax.set_ylim(min(df['Low']) - 1, max(df['High']) + 1)

    # Display info
    unrealized = holdings * (current_close - avg_buy_price) if holdings > 0 else 0
    total_value = balance + (holdings * current_close)
    ax.text(0.01, 0.95, f"Balance: £{balance:.2f}", transform=ax.transAxes, fontsize=10)
    ax.text(0.01, 0.90, f"Holdings: {holdings:.4f} oz", transform=ax.transAxes, fontsize=10)
    ax.text(0.01, 0.85, f"Lot Size: {lot_size}", transform=ax.transAxes, fontsize=10, color='blue')
    ax.text(0.01, 0.80, f"Avg Buy Price: £{avg_buy_price:.2f}", transform=ax.transAxes, fontsize=10)
    ax.text(0.01, 0.75, f"Unrealized PnL: £{unrealized:.2f}", transform=ax.transAxes, fontsize=10, color='green' if unrealized >= 0 else 'red')
    ax.text(0.01, 0.70, f"Total Value: £{total_value:.2f}", transform=ax.transAxes, fontsize=10)
    ax.text(0.01, 0.65, f"Last Action: {last_action}", transform=ax.transAxes, fontsize=10)

# === BUTTONS ===
ax_buy = plt.axes([0.7, 0.05, 0.1, 0.05])
ax_sell = plt.axes([0.81, 0.05, 0.1, 0.05])
btn_buy = Button(ax_buy, 'Buy')
btn_sell = Button(ax_sell, 'Sell')
btn_buy.on_clicked(buy)
btn_sell.on_clicked(sell)

fig.canvas.mpl_connect('key_press_event', on_key)
ani = FuncAnimation(fig, update, interval=100)
plt.tight_layout()
plt.show()