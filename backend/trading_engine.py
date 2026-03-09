import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TradingEngine")

class TradingEngine:
    """
    Implements the trading strategy:
    - 20 SMA Golden Cross
    - Buy Pressure Check
    """
    def __init__(self, sma_period: int = 20, buy_pressure_ratio: float = 1.5):
        self.sma_period = sma_period
        self.buy_pressure_ratio = buy_pressure_ratio
        self.price_history: List[float] = []

    def update_price(self, price: float):
        """Append new price tick."""
        self.price_history.append(price)
        # Keep only what we need to avoid memory leak
        if len(self.price_history) > self.sma_period * 2:
            self.price_history.pop(0)

    def calculate_sma(self) -> float:
        """Calculate the Simple Moving Average."""
        if len(self.price_history) < self.sma_period:
            return 0.0
        return sum(self.price_history[-self.sma_period:]) / self.sma_period

    def check_entry_signal(self, current_price: float, buy_volume: float, sell_volume: float) -> bool:
        """
        Check if we should enter a trade.
        Condition 1: Golden Cross (Price > 20 SMA)
        Condition 2: Buy Pressure > 1.5x Sell Pressure
        """
        sma = self.calculate_sma()
        if sma == 0.0:
            return False  # Not enough data

        # Golden Cross condition
        golden_cross = current_price > sma
        
        # Buy Pressure condition
        pressure_ok = sell_volume > 0 and (buy_volume / sell_volume) > self.buy_pressure_ratio

        if golden_cross and pressure_ok:
            logger.info(f"Entry Signal Detected! Price: {current_price}, SMA: {sma:.2f}")
            return True
            
        return False
