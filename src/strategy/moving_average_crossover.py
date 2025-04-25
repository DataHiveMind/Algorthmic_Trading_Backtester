# src/strategies/moving_average_crossover.py
import pandas as pd
from src.strategies.base_strategy import BaseStrategy

class MovingAverageCrossover(BaseStrategy):
    """
    A simple moving average crossover strategy.
    """
    def __init__(self, symbol, data: pd.DataFrame, params=None):
        super().__init__(symbol, data, params)
        self.short_window = self.params.get('short_window', 20)
        self.long_window = self.params.get('long_window', 50)

    def generate_signals(self):
        """
        Generates buy/sell signals based on short and long moving average crossover.
        """
        self.data['short_ma'] = self.data['Close'].rolling(window=self.short_window, min_periods=1).mean()
        self.data['long_ma'] = self.data['Close'].rolling(window=self.long_window, min_periods=1).mean()
        self.signals = pd.Series(0, index=self.data.index)  # Initialize with hold signals

        # Create buy signal
        self.signals[(self.data['short_ma'].shift(1) < self.data['long_ma'].shift(1)) & (self.data['short_ma'] > self.data['long_ma'])] = 1

        # Create sell signal
        self.signals[(self.data['short_ma'].shift(1) > self.data['long_ma'].shift(1)) & (self.data['short_ma'] < self.data['long_ma'])] = -1