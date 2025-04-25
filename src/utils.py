# src/utils.py
import numpy as np
import pandas as pd

def calculate_performance_metrics(returns, risk_free_rate=0.02):
    """
    Calculates common performance metrics for a series of returns.

    Args:
        returns (pd.Series): A Pandas Series of percentage returns.
        risk_free_rate (float): The annualized risk-free rate (default is 2%).

    Returns:
        dict: A dictionary containing the calculated performance metrics.
    """
    total_return = (1 + returns).prod() - 1
    annualized_return = ((1 + total_return)**(252/len(returns))) - 1 if len(returns) > 0 else 0  # Assuming 252 trading days
    excess_returns = returns - (risk_free_rate/252)
    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() > 0 else np.nan
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns / peak) - 1
    max_drawdown = drawdown.min() if len(drawdown) > 0 else 0

    metrics = {
        'Total Return': f'{total_return:.2%}',
        'Annualized Return': f'{annualized_return:.2%}',
        'Sharpe Ratio': f'{sharpe_ratio:.2f}',
        'Max Drawdown': f'{max_drawdown:.2%}'
    }
    return metrics

if __name__ == '__main__':
    # Example usage:
    returns_data = pd.Series([0.01, -0.005, 0.02, -0.01, 0.008])
    metrics = calculate_performance_metrics(returns_data)
    print(metrics)