import pytest

from src.stock_market import StockMarket


@pytest.fixture
def market():
    return StockMarket()


def test_calculate_dividend_yield_common(market):
    # Test for common stock
    assert market.calculate_dividend_yield("POP", 100) == 0.08  # 8 / 100


def test_calculate_dividend_yield_preferred(market):
    # Test for preferred stock
    assert market.calculate_dividend_yield("GIN", 100) == 0.02  # (2% of 100) / 100


def test_calculate_dividend_yield_zero_dividend(market):
    # Test for zero dividend
    assert market.calculate_dividend_yield("TEA", 100) == 0


def test_calculate_pe_ratio(market):
    assert market.calculate_pe_ratio("POP", 100) == 12.5  # 100 / 8


def test_record_trade(market):
    market.record_trade("POP", 100, 0, 500)
    assert len(market.trades) == 1
    assert market.trades[0]["stock_symbol"] == "POP"


def test_calculate_volume_weighted_stock_price(market):
    market.record_trade("POP", 100, 0, 500)
    market.record_trade("POP", 200, 0, 600)
    assert (
        market.calculate_volume_weighted_stock_price("POP") == 566.6666666666666
    )  # (500*100 + 600*200) / (100 + 200)


def test_dividend_yield_error_invalid_stock(market):
    with pytest.raises(ValueError):
        market.calculate_dividend_yield("XYZ", 100)


def test_pe_ratio_error_division_by_zero(market):
    with pytest.raises(ValueError):
        market.calculate_pe_ratio("TEA", 100)


def test_calculate_gbce_all_share_index(market):
    # Record some trades at the current time
    market.record_trade("POP", 100, 0, 500)
    market.record_trade("ALE", 200, 1, 300)

    # Ensure that the GBCE All Share Index can be calculated
    assert market.calculate_gbce_all_share_index() > 0


def test_calculate_gbce_all_share_index_no_recent_trades(market):
    # Assuming there are no trades in the last 15 minutes initially
    with pytest.raises(ValueError):
        market.calculate_gbce_all_share_index()
