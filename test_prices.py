import yfinance as yf
import sys

def test_price(symbol):
    print(f"Testing price for {symbol}...")
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            print(f"FAILED: No data for {symbol}")
            return
        
        current_price = data['Close'].iloc[-1]
        print(f"SUCCESS: {symbol} current price is {current_price}")
        print(f"Data range: {data.index[0]} to {data.index[-1]}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    test_price("BTC-USD")
    test_price("EURUSD=X")
    test_price("GC=F") # Gold
