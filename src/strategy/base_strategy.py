# src/strategies/base_strategy.py
import pandas as pd

class BaseStrategy:
    """
    A base class for trading strategies.
    """
    def __init__(self, symbol, data: pd.DataFrame, params=None):
        """
        Initializes the strategy.

        Args:
            symbol (str): The trading symbol.
            data (pd.DataFrame): The historical price data.
            params (dict, optional): Strategy-specific parameters. Defaults to None.
        """
        self.symbol = symbol
        self.data = data.copy()  # Avoid modifying the original DataFrame
        self.params = params if params is not None else {}
        self.signals = pd.Series(index=self.data.index)  # To store trading signals (1 for buy, -1 for sell, 0 for hold)

    def generate_signals(self):
        """
        Generates trading signals based on the historical data.
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement the generate_signals method.")

    def get_signals(self):
        """
        Returns the generated trading signals.
        """
        return self.signals