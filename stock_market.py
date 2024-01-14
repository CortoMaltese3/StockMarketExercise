from datetime import datetime, timedelta

from adapter import DataAdapter


class StockMarket:
    def __init__(self) -> None:
        self.data_adapter = DataAdapter()
        self.stocks = self.data_adapter.get_stocks()

        # Trade log
        self.trades = []

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
        try:
            stock = self.stocks[stock_symbol]
        except KeyError:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

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
        try:
            stock = self.stocks[stock_symbol]
        except KeyError:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        if not isinstance(price, (int, float)):
            raise TypeError("Price must be a number.")

        if price <= 0:
            raise ValueError("Price must be greater than zero.")

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
        if stock_symbol not in self.stocks:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        if not isinstance(share_quantity, int) or share_quantity <= 0:
            raise ValueError("Share quantity must be a positive integer.")

        if buy_sell_indicator not in [0, 1]:
            raise ValueError("Buy/sell indicator must be either 0 for 'buy' or 1 for 'sell'.")

        if not isinstance(traded_price, (int, float)) or traded_price <= 0:
            raise ValueError("Traded price must be a positive number.")

        self.trades.append(
            {
                "id": len(self.trades) + 1,
                "stock_symbol": stock_symbol,
                "transaction_created": datetime.utcnow(),
                "share_quantity": share_quantity,
                "buy_sell_indicator": buy_sell_indicator,
                "traded_price": traded_price,
            }
        )

    # Requirement 1a.iv
    def calculate_volume_weighted_stock_price(self, stock_symbol: str) -> float:
        """
        Calculate the Volume Weighted Stock Price (VWSP) based on trades in the past 15 minutes for a given stock.

        :param stock_symbol: Symbol of the stock (e.g., 'JOE').
        :return: The VWSP as a float.
        :raises ValueError: If the stock symbol is not found or there are no trades in the last 15 minutes.
        """
        if stock_symbol not in self.stocks:
            raise ValueError(f"Stock symbol '{stock_symbol}' not found.")

        recent_trades = [
            trade
            for trade in self.trades
            if trade["stock_symbol"] == stock_symbol
            and datetime.utcnow() - trade["transaction_created"] <= timedelta(minutes=15)
        ]

        total_quantity = sum(trade["share_quantity"] for trade in recent_trades)
        if total_quantity == 0:
            raise ValueError("No trades in the last 15 minutes for the given stock symbol.")

        total_traded_price_quantity = sum(
            trade["traded_price"] * trade["share_quantity"] for trade in recent_trades
        )

        return total_traded_price_quantity / total_quantity
