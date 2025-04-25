# src/backtester/backtester.py
import os
import pandas as pd
import matplotlib.pyplot as plt
from src.utils import calculate_performance_metrics

class Backtester:
    """
    A simple backtesting engine.
    """
    def __init__(self, symbol, data: pd.DataFrame, strategy, risk_manager, initial_capital=100000):
        """
        Initializes the backtester.

        Args:
            symbol (str): The trading symbol.
            data (pd.DataFrame): Historical price data with 'Close' column.
            strategy (BaseStrategy): The trading strategy object.
            risk_manager (BaseRiskManager): The risk management object.
            initial_capital (float): The initial trading capital.
        """
        self.symbol = symbol
        self.data = data
        self.strategy = strategy
        self.risk_manager = risk_manager
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = 0  # Number of shares/contracts held
        self.portfolio_value = pd.Series(index=self.data.index, dtype=float)
        self.transactions = pd.DataFrame(columns=['timestamp', 'symbol', 'action', 'quantity', 'price', 'value'])

    def run(self):
        """
        Runs the backtest.
        """
        self.strategy.generate_signals()
        signals = self.strategy.get_signals()
        self.portfolio_value.iloc[0] = self.initial_capital

        for i in range(1, len(self.data)):
            timestamp = self.data.index[i]
            price = self.data['Close'].iloc[i]
            previous_price = self.data['Close'].iloc[i-1]
            signal = signals.iloc[i]

            # Basic order execution (execute at the closing price of the day)
            order_quantity = 0

            if signal == 1:  # Buy signal
                order_quantity = self.risk_manager.calculate_position_size(signal, price) - self.positions
                if order_quantity > 0:
                    cost = order_quantity * price
                    if self.current_capital >= cost:
                        self.positions += order_quantity
                        self.current_capital -= cost
                        self._record_transaction(timestamp, 'BUY', order_quantity, price, cost)
                        self.risk_manager.update_on_trade(timestamp, self.symbol, order_quantity, price, is_entry=True)
            elif signal == -1: # Sell signal
                order_quantity = -min(self.positions, abs(self.risk_manager.calculate_position_size(signal, price))) # Close existing positions
                if order_quantity < 0:
                    proceeds = abs(order_quantity) * price
                    self.positions += order_quantity
                    self.current_capital += proceeds
                    self._record_transaction(timestamp, 'SELL', abs(order_quantity), price, proceeds)
                    self.risk_manager.update_on_trade(timestamp, self.symbol, order_quantity, price, is_entry=False)

            # Update portfolio value
            self.portfolio_value.iloc[i] = self.current_capital + (self.positions * price)

        # Calculate returns and performance metrics
        self.portfolio_returns = self.portfolio_value.pct_change().dropna()
        self.performance_metrics = calculate_performance_metrics(self.portfolio_returns)
        print("Backtest Completed.")
        print("Performance Metrics:")
        for key, value in self.performance_metrics.items():
            print(f"  {key}: {value}")
        results_dir = 'results'
        os.makedirs(results_dir, exist_ok=True)
        timestamp_str = pd.Timestamp('now').strftime("%Y%m%d_%H%M%S")
        base_filename = f"{self.symbol}_{self.strategy.__class__.__name__}_{self.risk_manager.__class__.__name__}_{timestamp_str}"

        # Save Performance Metrics
        with open(os.path.join(results_dir, f"{base_filename}_performance.txt"), 'w') as f:
            f.write("Performance Metrics:\n")
            for key, value in self.performance_metrics.items():
                f.write(f"  {key}: {value}\n")
            f.write("\nTransactions:\n")
            f.write(self.transactions.to_string())

        # Save Transactions to CSV
        self.transactions.to_csv(os.path.join(results_dir, f"{base_filename}_transactions.csv"), index=False)

        # Save Portfolio Value Plot
        plt.figure(figsize=(12, 6))
        plt.plot(self.portfolio_value, label='Portfolio Value')
        plt.title(f'{self.symbol} Backtest - Portfolio Value')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(results_dir, f"{base_filename}_portfolio_value.png"))
        plt.close()

        # Save Drawdown Plot
        cumulative_returns = (1 + self.portfolio_returns).cumprod()
        peak = cumulative_returns.expanding(min_periods=1).max()
        drawdown = (cumulative_returns / peak) - 1
        plt.figure(figsize=(12, 6))
        plt.plot(drawdown, label='Drawdown')
        plt.title(f'{self.symbol} Backtest - Drawdown')
        plt.xlabel('Date')
        plt.ylabel('Drawdown')
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(results_dir, f"{base_filename}_drawdown.png"))
        plt.close()

        print(f"\nBacktest results saved to the 'results/' folder.")

        print("\nTransactions:")
        print(self.transactions)

    def _record_transaction(self, timestamp, action, quantity, price, value):
        """
        Records a transaction.
        """
        self.transactions = pd.concat([self.transactions, pd.DataFrame([{
            'timestamp': timestamp,
            'symbol': self.symbol,
            'action': action,
            'quantity': quantity,
            'price': price,
            'value': value
        }])], ignore_index=True)

# Example usage (to be moved to a separate run script later):
if __name__ == '__main__':
    from src.data_loader import download_data
    from src.strategy.moving_average_crossover import MovingAverageCrossover
    from src.risk_management.fixed_position_sizing import FixedPositionSizing

    symbol = 'AAPL'
    start_date = '2020-01-01'
    end_date = '2023-12-31'
    download_data(symbol, start_date, end_date)
    data = pd.read_csv(f'data/{symbol}.csv', index_col='Date', parse_dates=True)

    # Simple Moving Average Crossover Strategy
    strategy_params = {'short_window': 20, 'long_window': 50}
    strategy = MovingAverageCrossover(symbol, data, params=strategy_params)

    # Fixed Position Sizing Risk Management (e.g., buy 10 shares per trade)
    risk_manager = FixedPositionSizing(position_size=10, initial_capital=100000)

    backtester = Backtester(symbol, data, strategy, risk_manager, initial_capital=100000)
    backtester.run()