import yfinance as yf
from typing import List
from app.domain.candle import Candle
from app.infrastructure.providers.base import BaseDataProvider
from datetime import datetime

class YahooFinanceProvider(BaseDataProvider):
    async def fetch_candles(self, symbol: str, timeframe: str, limit: int = 100) -> List[Candle]:
        # Mapear símbolos para o formato do Yahoo Finance
        # Forex: EURUSD=X, Metais: GC=F (Ouro), etc.
        ticker_symbol = self._map_symbol(symbol)
        
        # Mapear timeframe
        interval = self._map_timeframe(timeframe)
        
        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(period="5d", interval=interval)
        
        if df.empty:
            raise Exception(f"Nenhum dado encontrado para o símbolo {symbol}")
            
        df = df.tail(limit)
        
        candles = []
        for index, row in df.iterrows():
            candles.append(Candle(
                timestamp=index.to_pydatetime(),
                open=float(row['Open']),
                high=float(row['High']),
                low=float(row['Low']),
                close=float(row['Close']),
                volume=float(row['Volume'])
            ))
        return candles

    def _map_symbol(self, symbol: str) -> str:
        # Lógica de mapeamento para o Yahoo
        symbol = symbol.upper()
        if len(symbol) == 6 and symbol not in ["BTCUSD", "ETHUSD"]: # Provável par Forex
            return f"{symbol}=X"
        if symbol in ["GOLD", "XAUUSD"]:
            return "GC=F"
        if symbol in ["SILVER", "XAGUSD"]:
            return "SI=F"
        return symbol

    def _map_timeframe(self, timeframe: str) -> str:
        mapping = {
            "1m": "1m", "5m": "5m", "15m": "15m", "1h": "1h", "4h": "1h", "1d": "1d"
        }
        return mapping.get(timeframe, "1h")
