# src/risk_management/fixed_position_sizing.py
from src.risk_management.base_risk_manager import BaseRiskManager

class FixedPositionSizing(BaseRiskManager):
    """
    A simple risk manager that buys/sells a fixed number of shares/contracts per trade.
    """
    def __init__(self, position_size=10, initial_capital=100000):
        super().__init__(initial_capital)
        self.position_size = position_size

    def update_on_trade(self, timestamp, symbol, quantity, price, is_entry):
        # For this simple risk manager, we don't need to track much state
        pass

    def calculate_position_size(self, signal, price):
        """
        Returns the fixed position size based on the signal.
        """
        if signal == 1:  # Buy
            return self.position_size
        elif signal == -1: # Sell (close all existing)
            return 0 # We'll handle closing in the backtester for simplicity
        return 0