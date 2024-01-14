"""
Requirements:
Provide working source code that will :
a. For a given stock, 
    i.   Given any price as input, calculate the dividend yield
    ii.  Given any price as input, calculate the P/E Ratio
    iii. Record a trade, with timestamp, quantity of shares, buy or sell indicator and 
         traded price
    iv. Calculate Volume Weighted Stock Price based on trades in past 15 minutes
b. Calculate the GBCE All Share Index using the geometric mean of prices for all stocks
"""


from datetime import datetime, timedelta
import math


# Sample data from the Global Beverage Corporation Exchange
stocks = {
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

trades = []


# Requirement 1a.i
def calculate_dividend_yield(stock_symbol, price):
    """
    Calculate the dividend yield for a given stock and price.
    """
    try:
        stock = stocks[stock_symbol]
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
def calculate_pe_ratio(stock_symbol, price):
    """
    Calculate the P/E ratio for a given stock and price.
    """
    try:
        stock = stocks[stock_symbol]
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
def record_trade(stock_symbol, share_quantity, buy_sell_indicator, traded_price):
    """
    Record a trade, with timestamp, quantity of shares, buy or sell indicator and
    traded price.
    """
    trades.append(
        {
            "id": len(trades) + 1,
            "stock_symbol": stock_symbol,
            "transaction_created": datetime.utcnow(),
            "share_quantity": share_quantity,
            "buy_sell_indicator": buy_sell_indicator,  # 0 for 'buy' or 1 for 'sell'
            "traded_price": traded_price,
        }
    )


# Requirement 1a.iv
def calculate_volume_weighted_stock_price(stock_symbol):
    """
    Calculate Volume Weighted Stock Price based on trades in past 15 minutes.
    """
    recent_trades = [
        trade
        for trade in trades
        if trade["stock_symbol"] == stock_symbol
        and datetime.utcnow() - trade["transaction_created"] <= timedelta(minutes=15)
    ]
    total_traded_price_quantity = sum(
        trade["traded_price"] * trade["share_quantity"] for trade in recent_trades
    )
    total_quantity = sum(trade["share_quantity"] for trade in recent_trades)
    if total_quantity == 0:
        return None
    return total_traded_price_quantity / total_quantity


def main():
    # Divident yield
    print(calculate_dividend_yield("TEA", 100))
    print(calculate_dividend_yield("ALE", 100))
    print(calculate_dividend_yield("GIN", 100))

    # P/E ratio
    # print(calculate_pe_ratio("TEA", 100))
    print(calculate_pe_ratio("ALE", 100))
    print(calculate_pe_ratio("GIN", 100))

    record_trade("GEO", 200, 0, 500)
    record_trade("GEO", 100, 1, 300)
    print(trades)

    print(calculate_volume_weighted_stock_price("GEO"))


if __name__ == "__main__":
    main()
