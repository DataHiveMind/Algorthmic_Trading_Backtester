# src/risk_management/base_risk_manager.py
import pandas as pd

class BaseRiskManager:
    """
    A base class for risk management modules.
    """
    def __init__(self, initial_capital=100000):
        """
        Initializes the risk manager.

        Args:
            initial_capital (float): The initial trading capital.
        """
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}  # Dictionary to track current positions (symbol: quantity)
        self.trade_history = [] # List to store trade details

    def update_on_trade(self, timestamp, symbol, quantity, price, is_entry):
        """
        Updates the risk manager's state after a trade.

        Args:
            timestamp (pd.Timestamp): The timestamp of the trade.
            symbol (str): The trading symbol.
            quantity (int): The quantity of shares/contracts traded.
            price (float): The price at which the trade was executed.
            is_entry (bool): True if it's an entry trade, False if it's an exit.
        """
        raise NotImplementedError("Subclasses must implement the update_on_trade method.")

    def calculate_position_size(self, signal, price):
        """
        Calculates the position size based on the signal and current capital.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the calculate_position_size method.")