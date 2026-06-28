import yfinance as yf
import httpx
from typing import List
from app.domain.candle import Candle
from app.infrastructure.providers.base import BaseDataProvider
from datetime import datetime, timezone, timedelta


# ── Crypto → Binance (real-time, gratuito, sem API key) ──────────────────────
BINANCE_MAP = {
    "BTCUSD": "BTCUSDT",
    "ETHUSD": "ETHUSDT",
    "BNBUSD": "BNBUSDT",
    "SOLUSD": "SOLUSDT",
}

# ── Índices (Yahoo Finance — Futuros) ─────────────────────────────────────────
INDEX_MAP = {
    "NQ100":  "NQ=F",    "NAS100": "NQ=F",   "NASDAQ": "NQ=F",
    "USTEC":  "NQ=F",    "NQ":     "NQ=F",
    "SP500":  "ES=F",    "US500":  "ES=F",   "SPX":    "ES=F",
    "DOW":    "YM=F",    "US30":   "YM=F",
    "DAX":    "FDAX=F",  "GER40":  "FDAX=F",
}

# ── Metais ────────────────────────────────────────────────────────────────────
METALS_MAP = {
    "GOLD":   "GC=F",  "XAUUSD": "GC=F",
    "SILVER": "SI=F",  "XAGUSD": "SI=F",
    "OIL":    "CL=F",  "USOIL":  "CL=F",
}

# ── Top Forex (Yahoo: EURUSD=X) ───────────────────────────────────────────────
FOREX_PAIRS = {
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "AUDUSD",
    "USDCAD", "NZDUSD", "EURGBP", "EURJPY", "GBPJPY",
}

HOURS_PER_CANDLE = {
    "1m": 1/60, "5m": 5/60, "15m": 15/60, "30m": 30/60,
    "1h": 1.0,  "4h": 4.0,  "1d": 24.0,
}


class YahooFinanceProvider(BaseDataProvider):

    async def fetch_candles(self, symbol: str, timeframe: str, limit: int = 100) -> List[Candle]:
        sym = symbol.upper()
        if sym in BINANCE_MAP:
            return await self._from_binance(sym, timeframe, limit)
        return await self._from_yahoo(sym, timeframe, limit)

    # ── Binance ───────────────────────────────────────────────────────────────
    async def _from_binance(self, symbol: str, timeframe: str, limit: int) -> List[Candle]:
        """Binance suporta 1m/5m/15m/30m/1h/4h/1d nativamente."""
        url = "https://api.binance.com/api/v3/klines"
        params = {
            "symbol": BINANCE_MAP[symbol],
            "interval": timeframe,   # Binance aceita "4h" diretamente
            "limit": limit,
        }
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

        return [
            Candle(
                timestamp=datetime.fromtimestamp(k[0] / 1000, tz=timezone.utc),
                open=float(k[1]),
                high=float(k[2]),
                low=float(k[3]),
                close=float(k[4]),
                volume=float(k[5]),
            )
            for k in data
        ]

    # ── Yahoo Finance ─────────────────────────────────────────────────────────
    async def _from_yahoo(self, symbol: str, timeframe: str, limit: int) -> List[Candle]:
        """
        yfinance NÃO suporta intervalo '4h'.
        Para 4H: busca 1H e reamostrar via pandas resample.
        """
        ticker_symbol = self._resolve_yahoo_symbol(symbol)
        is_4h = timeframe == "4h"
        yf_interval = "1h" if is_4h else self._yf_interval(timeframe)

        # Datas explícitas → evita cache do yfinance
        end = datetime.now(tz=timezone.utc)
        hours = HOURS_PER_CANDLE.get(timeframe, 1.0)
        fetch_n = (limit * 5) if is_4h else int(limit * 1.5)
        start = end - timedelta(hours=max(hours * fetch_n, 48))

        ticker = yf.Ticker(ticker_symbol)
        df = ticker.history(start=start, end=end, interval=yf_interval, auto_adjust=True)

        if df.empty:
            raise Exception(f"Sem dados para {symbol} ({ticker_symbol})")

        # Resample 1H → 4H
        if is_4h:
            df = (
                df.resample("4h")
                .agg({"Open": "first", "High": "max", "Low": "min",
                      "Close": "last", "Volume": "sum"})
                .dropna()
            )

        df = df.tail(limit)

        candles = []
        for index, row in df.iterrows():
            ts = index.to_pydatetime()
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=timezone.utc)
            candles.append(Candle(
                timestamp=ts,
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Min"] if "Min" in row else row["Low"]),
                close=float(row["Close"]),
                volume=float(row["Volume"]),
            ))
        return candles

    # ── Resolução de símbolo Yahoo ─────────────────────────────────────────────
    def _resolve_yahoo_symbol(self, symbol: str) -> str:
        sym = symbol.upper()
        if sym in INDEX_MAP:
            return INDEX_MAP[sym]
        if sym in METALS_MAP:
            return METALS_MAP[sym]
        # Forex: 6 chars alfabéticos → EURUSD=X
        if sym in FOREX_PAIRS or (len(sym) == 6 and sym.isalpha()):
            return f"{sym}=X"
        return sym

    def _yf_interval(self, timeframe: str) -> str:
        return {
            "1m": "1m", "5m": "5m", "15m": "15m",
            "30m": "30m", "1h": "1h", "1d": "1d",
        }.get(timeframe, "1h")
