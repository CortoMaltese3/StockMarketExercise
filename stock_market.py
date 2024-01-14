from datetime import datetime, timedelta


class StockMarket:
    def __init__(self) -> None:
        # Sample data from the Global Beverage Corporation Exchange
        self.stocks = {
            "TEA": {
                "Type": "Common",
                "Last Dividend": 0,
                "Fixed Dividend": 0,
                "Par Value": 100,
            },
            "POP": {
                "Type": "Common",
                "Last Dividend": 8,
                "Fixed Dividend": 0,
                "Par Value": 100,
            },
            "ALE": {
                "Type": "Common",
                "Last Dividend": 23,
                "Fixed Dividend": 0,
                "Par Value": 60,
            },
            "GIN": {
                "Type": "Preferred",
                "Last Dividend": 8,
                "Fixed Dividend": "2%",
                "Par Value": 100,
            },
            "JOE": {
                "Type": "Common",
                "Last Dividend": 13,
                "Fixed Dividend": 0,
                "Par Value": 250,
            },
        }

        # Trade log
        self.trades = []

    # Requirement 1a.i
    def calculate_dividend_yield(self, stock_symbol, price):
        """
        Calculate the dividend yield for a given stock and price.
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
    def calculate_pe_ratio(self, stock_symbol, price):
        """
        Calculate the P/E ratio for a given stock and price.
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
    def record_trade(self, stock_symbol, share_quantity, buy_sell_indicator, traded_price):
        """
        Record a trade, with timestamp, quantity of shares, buy or sell indicator, and
        traded price.
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
    def calculate_volume_weighted_stock_price(self, stock_symbol):
        """
        Calculate Volume Weighted Stock Price based on trades in past 15 minutes.
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
