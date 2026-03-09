import asyncio
import logging
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List

from backend.broker_api import KoreaInvestmentBrokerAPI
from backend.risk_management import RiskManager
from backend.trading_engine import TradingEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

app = FastAPI(title="KRX Gold Auto Trader")

# Instances
broker = KoreaInvestmentBrokerAPI()
risk_manager = RiskManager()
trading_engine = TradingEngine()

# State
is_trading_active = False

@app.on_event("startup")
async def startup_event():
    logger.info("Starting background trading loop...")
    asyncio.create_task(trading_loop())

async def trading_loop():
    global is_trading_active
    while True:
        try:
            # 1. Fetch Market Data
            market_data = await broker.get_market_data()
            current_price = market_data["current_price"]
            buy_vol = market_data["buy_bids_volume"]
            sell_vol = market_data["sell_asks_volume"]
            
            # Update engine
            trading_engine.update_price(current_price)
            
            # 2. Fetch Account Data
            account = await broker.get_account_status()
            balance = account["balance"]
            positions = account["positions"]
            
            # 3. Check Risk Management (Exits)
            if is_trading_active and positions:
                for pos in list(positions):
                    entry = pos["entry_price"]
                    amount = pos["amount_grams"]
                    
                    exit_signal = risk_manager.check_exit_conditions(entry, current_price)
                    if exit_signal in ['TP', 'SL']:
                        logger.info(f"Executing {exit_signal} Sell! Entry: {entry}, Current: {current_price}")
                        await broker.execute_trade("SELL", amount_grams=amount)
            
            # 4. Check Strategy (Entries)
            elif is_trading_active and not positions:
                if trading_engine.check_entry_signal(current_price, buy_vol, sell_vol):
                    alloc_krw = risk_manager.calculate_position_size(balance)
                    logger.info(f"Entry Signal! Buying for KRW {alloc_krw}")
                    if alloc_krw > 0:
                        await broker.execute_trade("BUY", amount_krw=alloc_krw)
                        
        except Exception as e:
            logger.error(f"Error in trading loop: {e}")
            
        await asyncio.sleep(2)  # Tick every 2 seconds for mockup speed

# API Endpoints
@app.get("/api/status")
async def get_status():
    market = await broker.get_market_data()
    account = await broker.get_account_status()
    sma = trading_engine.calculate_sma()
    
    return {
        "status": "active" if is_trading_active else "paused",
        "market": market,
        "sma": round(sma, 2),
        "account": account
    }

@app.post("/api/toggle")
async def toggle_trading():
    global is_trading_active
    is_trading_active = not is_trading_active
    return {"status": "active" if is_trading_active else "paused"}

# Allow serving static UI later
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
