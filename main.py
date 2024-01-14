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


def main():
    # Divident yield
    print(calculate_dividend_yield("TEA", 100))
    print(calculate_dividend_yield("ALE", 100))
    print(calculate_dividend_yield("GIN", 100))

    # P/E ratio
    print(calculate_pe_ratio("TEA", 100))
    print(calculate_pe_ratio("ALE", 100))
    print(calculate_pe_ratio("GIN", 100))


if __name__ == "__main__":
    main()
