import yfinance as yf
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List, Dict, Any

app = FastAPI(title="ICT Market Intelligence - Probabilistic Engine v2.0")

# Habilitar CORS para o Lovable.dev e outros frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mapeamento de símbolos comuns
SYMBOL_MAP = {
    "BTCUSD": "BTC-USD",
    "BTC": "BTC-USD",
    "EURUSD": "EURUSD=X",
    "GOLD": "GC=F",
    "SP500": "^GSPC",
    "NAS100": "^IXIC",
    "NQ100": "^IXIC"
}

@app.get("/")
async def root():
    return {
        "status": "online", 
        "project": "ICT Market Intelligence",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health():
    return {"status": "ok", "service": "probabilistic-engine"}

@app.get("/symbols")
async def get_symbols():
    """Retorna a lista de símbolos suportados."""
    return [
        {"id": "BTCUSD", "name": "Bitcoin / USD", "category": "Criptomoedas"},
        {"id": "EURUSD", "name": "Euro / USD", "category": "Câmbio"},
        {"id": "NQ100", "name": "Nasdaq 100", "category": "Índices"},
        {"id": "GOLD", "name": "Ouro", "category": "Metais"}
    ]

@app.get("/price/{symbol}")
@app.get("/api/price/{symbol}")
async def get_price(symbol: str):
    original_symbol = symbol.upper()
    yf_symbol = SYMBOL_MAP.get(original_symbol, original_symbol)
    
    try:
        ticker = yf.Ticker(yf_symbol)
        data = ticker.history(period="1d", interval="1m")
        if data.empty:
            data = ticker.history(period="1d", interval="5m")
            
        if data.empty:
            raise HTTPException(status_code=404, detail=f"No data found for symbol {yf_symbol}")
            
        current_price = data['Close'].iloc[-1]
        open_price = data['Open'].iloc[0]
        change = current_price - open_price
        pct_change = (change / open_price) * 100
        
        return {
            "symbol": original_symbol,
            "price": round(float(current_price), 5),
            "change": round(float(change), 5),
            "pct_change": round(float(pct_change), 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/{symbol}")
@app.get("/api/analysis/{symbol}")
async def get_analysis(symbol: str):
    symbol = symbol.upper()
    
    # Simulação de análise baseada no preço real
    price_data = await get_price(symbol)
    price = price_data["price"]
    
    narratives = {
        "BTCUSD": f"BTCUSD em ${price}: PO3 em acumulação concluída na sessão asiática. Londres expandindo para liquidez externa em PDH; aguardando manipulação para entrada em OB H1.",
        "NQ100": f"NQ100 em ${price}: Rejeição em H4 FVG. Preço buscando Internal Liquidity. Viés de baixa para a sessão de NY.",
        "EURUSD": f"EURUSD em ${price}: Consolidação acima do Dealing Range Equilibrium."
    }
    
    return {
        "symbol": symbol,
        "price": price,
        "bias": "Otimista" if "BTC" in symbol or "NQ" in symbol else "Neutra",
        "confidence": 74.0,
        "phase": "Reprecificação",
        "narrative": narratives.get(symbol, f"{symbol} em ${price}: Análise em processamento."),
        "zones_active": 0,
        "decomposition": {
            "structural": 82,
            "liquidity": 65,
            "momentum": 70
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
