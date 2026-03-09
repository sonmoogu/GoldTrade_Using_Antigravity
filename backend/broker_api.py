import random
import asyncio
from typing import Dict, Any

import httpx

class KoreaInvestmentBrokerAPI:
    """
    Implementation of Korea Investment & Securities (KIS) API.
    Fetches real-time WebSocket connection key and provides simulated data.
    """
    def __init__(self, use_mock: bool = True):
        # API Keys provided in user image
        self.appkey = "PSg5dctL9dKPo727j1JUr405OSXXXXXXXXX"
        self.secretkey = "vo2I8zS68zpdjGuWVfyM9VikjxE0I0CbgPEamnqPA00G0bIfrefQb2RUD1xP7SqatQXr1cD1fGUNsb78MVXoq6o4IAYt0YTiHajbMoFy+c72kbqSowQY1Pvp39/x6ejpJJXCj7gE3yVOB/h2SHvJ+URmYeBTfrQoOqJAOYc/DkXXXXXXXXXX"
        self.domain = "https://openapivts.koreainvestment.com:29443" if use_mock else "https://openapi.koreainvestment.com:9443"
        self.approval_key = None

        self.current_price = 105000  # Initial KRX Gold price per gram
        self.balance = 10000000     # 10,000,000 KRW initially
        self.gold_inventory = 0     # Grams of gold owned
        self.positions = []         # List of dicts: {'entry_price': ..., 'amount': ...}

    async def get_websocket_approval_key(self) -> str:
        """Fetches the real-time (WebSocket) connection access key via REST."""
        if self.approval_key:
            return self.approval_key
            
        url = f"{self.domain}/oauth2/Approval"
        headers = {"content-type": "application/json; utf-8"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.appkey,
            "secretkey": self.secretkey
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=body)
                data = response.json()
                if "approval_key" in data:
                    self.approval_key = data["approval_key"]
                    print(f"Successfully obtained KIS WebSocket Approval Key: {self.approval_key}")
                else:
                    print(f"Failed to obtain KIS Approval Key: {data}")
            except Exception as e:
                print(f"HTTP request failed: {e}")
                
        return self.approval_key

    async def get_market_data(self) -> Dict[str, Any]:
        """Simulates fetching real-time market data"""
        # Fetch the websocket key dynamically (simulating step 3-2)
        if not self.approval_key:
            await self.get_websocket_approval_key()
            
        # Random walk for price
        change = random.uniform(-100, 100)
        self.current_price += change
        
        # Simulate order book pressure
        buy_bids_volume = random.uniform(1000, 5000)
        sell_asks_volume = random.uniform(1000, 5000)
        
        return {
            "current_price": round(self.current_price, 2),
            "buy_bids_volume": round(buy_bids_volume, 2),
            "sell_asks_volume": round(sell_asks_volume, 2)
        }

    async def get_account_status(self) -> Dict[str, Any]:
        """Simulates fetching account balance and inventory"""
        return {
            "balance": round(self.balance, 2),
            "gold_inventory": self.gold_inventory,
            "positions": self.positions
        }

    async def execute_trade(self, action: str, amount_krw: float = 0, amount_grams: float = 0) -> Dict[str, Any]:
        """Simulates executing a buy or sell order"""
        if action == "BUY":
            grams_to_buy = amount_krw / self.current_price
            if self.balance >= amount_krw:
                self.balance -= amount_krw
                self.gold_inventory += grams_to_buy
                self.positions.append({
                    "entry_price": self.current_price,
                    "amount_grams": grams_to_buy
                })
                return {"status": "SUCCESS", "message": f"Bought {grams_to_buy:.2f}g at {self.current_price:.2f}"}
            else:
                return {"status": "FAILED", "message": "Insufficient funds"}
                
        elif action == "SELL":
            if self.gold_inventory >= amount_grams:
                revenue = amount_grams * self.current_price
                self.balance += revenue
                self.gold_inventory -= amount_grams
                
                # Simple position resolution for mock (removes all for simplicity if selling all)
                if self.gold_inventory < 0.01:
                    self.positions = []
                    self.gold_inventory = 0
                
                return {"status": "SUCCESS", "message": f"Sold {amount_grams:.2f}g at {self.current_price:.2f}"}
            else:
                return {"status": "FAILED", "message": "Insufficient gold inventory"}
        
        return {"status": "FAILED", "message": "Unknown action"}
