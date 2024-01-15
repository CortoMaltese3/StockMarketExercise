from datetime import datetime, timedelta

import pandas as pd

from .adapter import DataAdapter


class StockMarket:
    def __init__(self) -> None:
        # Initialize the data adapter to fetch stock data
        self.data_adapter = DataAdapter()
        self._stocks = self.data_adapter.get_stocks()
        # Convert the stock data into a Pandas DataFrame for easier manipulation
        self.stocks_df = self._convert_stocks_to_dataframe()

        # Trade log
        # Initialize the trades DataFrame with predefined columns to avoid issues with empty DataFrames
        self.trades = pd.DataFrame(
            columns=[
                "id",
                "stock_symbol",
                "transaction_created",
                "share_quantity",
                "buy_sell_indicator",
                "traded_price",
            ]
        )

    def _convert_stocks_to_dataframe(self) -> pd.DataFrame:
        """
        Convert the stocks dictionary to a DataFrame.

        :return: The stocks DataFrame.
        """
        return pd.DataFrame.from_dict(self._stocks, orient="index")

    # Requirement 1a.i
    def calculate_dividend_yield(self, stock_symbol: str, price: float) -> float:
        """
        Calculate the dividend yield for a given stock and price.

        :param stock_symbol: Symbol of the stock (e.g., 'TEA').
        :param price: The market price of the stock.
        :return: The dividend yield as a float.
        :raises ValueError: If the stock symbol is not found or the price is non-positive.
        :raises TypeError: If the price is not a number.
        """
        # Invalid input error handling
        if stock_symbol not in self.stocks_df.index:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        # Retrieve single stock information from the dataset
        stock = self.stocks_df.loc[stock_symbol]

        # Calculate dividend yield based on stock type
        if stock["Type"] == "Common":
            if stock["Last Dividend"] == 0:
                return 0
            return stock["Last Dividend"] / price
        else:  # Preferred stock
            fixed_dividend = float(stock["Fixed Dividend"].strip("%")) / 100
            return fixed_dividend * stock["Par Value"] / price

    # Requirement 1a.ii
    def calculate_pe_ratio(self, stock_symbol: str, price: float) -> float:
        """
        Calculate the Price/Earnings (P/E) ratio for a given stock and price.

        :param stock_symbol: Symbol of the stock (e.g., 'ALE').
        :param price: The market price of the stock.
        :return: The P/E ratio as a float.
        :raises ValueError: If the stock symbol is not found, the price is non-positive,
                            or the last dividend is zero.
        :raises TypeError: If the price is not a number.
        """
        # Invalid input error handling
        if stock_symbol not in self.stocks_df.index:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

        # Retrieve single stock information from the dataset
        stock = self.stocks_df.loc[stock_symbol]
        if stock["Last Dividend"] == 0:
            raise ValueError("P/E ratio cannot be calculated. Error division by zero.")

        return price / stock["Last Dividend"]

    # Requirement 1a.iii
    def record_trade(
        self, stock_symbol: str, share_quantity: int, buy_sell_indicator: int, traded_price: float
    ):
        """
        Record a trade with details such as stock symbol, quantity of shares, buy/sell indicator, and traded price.

        :param stock_symbol: Symbol of the stock (e.g., 'GIN').
        :param share_quantity: The number of shares traded.
        :param buy_sell_indicator: Indicator of the trade type (0 for 'buy', 1 for 'sell').
        :param traded_price: The price at which the stock was traded.
        :raises ValueError: If the stock symbol is not found, share quantity is non-positive,
                            buy/sell indicator is not 0 or 1, or traded price is non-positive.
        :raises TypeError: If the share quantity or traded price is not a number.
        """
        # Invalid input error handling
        if stock_symbol not in self.stocks_df.index:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        if not isinstance(share_quantity, int) or share_quantity <= 0:
            raise ValueError("Share quantity must be a positive integer.")

        if buy_sell_indicator not in [0, 1]:
            raise ValueError("Buy/sell indicator must be either 0 for 'buy' or 1 for 'sell'.")

        if not isinstance(traded_price, (int, float)) or traded_price <= 0:
            raise ValueError("Traded price must be a positive number.")

        # Record the trade
        new_trade = pd.DataFrame(
            [
                {
                    "id": len(self.trades) + 1,
                    "stock_symbol": stock_symbol,
                    "transaction_created": datetime.utcnow(),
                    "share_quantity": share_quantity,
                    "buy_sell_indicator": buy_sell_indicator,
                    "traded_price": traded_price,
                }
            ]
        )

        # Concatenate the new trade to the existing trades DataFrame
        self.trades = pd.concat([self.trades, new_trade], ignore_index=True)

    # Requirement 1a.iv
    def calculate_volume_weighted_stock_price(self, stock_symbol: str) -> float:
        """
        Calculate the Volume Weighted Stock Price (VWSP) based on trades in the past 15 minutes for a given stock.

        :param stock_symbol: Symbol of the stock (e.g., 'JOE').
        :return: The VWSP as a float.
        :raises ValueError: If the stock symbol is not found or there are no trades in the last 15 minutes.
        """
        # Invalid input error handling
        if stock_symbol not in self.stocks_df.index:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        # Retrieve recent trades for the given stock
        trades_df = pd.DataFrame(self.trades)
        recent_trades = trades_df[
            (trades_df["stock_symbol"] == stock_symbol)
            & (datetime.utcnow() - trades_df["transaction_created"] <= timedelta(minutes=15))
        ]

        # Raise error in case of no trades in the last 15 minutes
        if recent_trades.empty:
            raise ValueError("No trades in the last 15 minutes for the given stock symbol.")

        # Calculate the VWSP
        volume_weighted_stock_price = (
            recent_trades["traded_price"] * recent_trades["share_quantity"]
        ).sum() / recent_trades["share_quantity"].sum()

        return volume_weighted_stock_price

    # Requirement 1b
    def calculate_gbce_all_share_index(self) -> float:
        """
        Calculate the GBCE All Share Index using the geometric mean of traded prices for all stocks in the last 15 minutes.

        :return: The GBCE All Share Index as a float.
        :raises ValueError: If there are no trades in the last 15 minutes.
        """
        # Retrieve recent trades
        trades_df = pd.DataFrame(self.trades)
        recent_prices = trades_df[
            datetime.utcnow() - trades_df["transaction_created"] <= timedelta(minutes=15)
        ]["traded_price"]

        # Raise error in case of no trades in the last 15 minutes
        if recent_prices.empty:
            raise ValueError(
                "No trades in the last 15 minutes to calculate the GBCE All Share Index."
            )

        # Calculate the GBCE All Share Index
        product_of_prices = recent_prices.prod()

        return product_of_prices ** (1 / len(recent_prices))
