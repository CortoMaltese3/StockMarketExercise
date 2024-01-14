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

from stock_market import StockMarket


def main():
    market = StockMarket()

    # Dividend yield
    print(market.calculate_dividend_yield("TEA", 100))
    print(market.calculate_dividend_yield("ALE", 100))
    print(market.calculate_dividend_yield("GIN", 100))

    # P/E ratio
    print(market.calculate_pe_ratio("ALE", 100))
    print(market.calculate_pe_ratio("GIN", 100))

    market.record_trade("ALE", 200, 0, 500)
    market.record_trade("ALE", 100, 1, 300)
    print(market.trades)

    print(market.calculate_volume_weighted_stock_price("ALE"))

    print(market.calculate_gbce_all_share_index())


if __name__ == "__main__":
    main()
