class RiskManager:
    """
    Handles risk management rules:
    - Max 15% of capital per trade
    - Take Profit (TP) at +4.5%
    - Stop Loss (SL) at -2.0%
    """
    def __init__(self, max_capital_pct=0.15, take_profit_pct=0.045, stop_loss_pct=-0.02):
        self.max_capital_pct = max_capital_pct
        self.take_profit_pct = take_profit_pct
        self.stop_loss_pct = stop_loss_pct

    def calculate_position_size(self, balance: float) -> float:
        """Calculate max KRW to allocate for a single trade."""
        return balance * self.max_capital_pct

    def check_exit_conditions(self, entry_price: float, current_price: float) -> str:
        """
        Evaluates whether a position should be sold based on TP or SL.
        Returns 'TP', 'SL', or 'HOLD'.
        """
        if entry_price <= 0:
            return 'HOLD'
            
        profit_pct = (current_price - entry_price) / entry_price
        
        if profit_pct >= self.take_profit_pct:
            return 'TP'
        elif profit_pct <= self.stop_loss_pct:
            return 'SL'
            
        return 'HOLD'
