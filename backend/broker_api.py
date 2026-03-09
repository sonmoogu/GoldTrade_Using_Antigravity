import random
import asyncio
from typing import Dict, Any

class MockBrokerAPI:
    """
    Mock implementation of Samsung Securities API (mPOP).
    Provides real-time simulated spot prices, best bids, and asks.
    """
    def __init__(self):
        self.current_price = 105000  # Initial KRX Gold price per gram
        self.balance = 10000000     # 10,000,000 KRW initially
        self.gold_inventory = 0     # Grams of gold owned
        self.positions = []         # List of dicts: {'entry_price': ..., 'amount': ...}

    async def get_market_data(self) -> Dict[str, Any]:
        """Simulates fetching real-time market data"""
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
