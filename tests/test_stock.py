from unittest.mock import patch, MagicMock
import pytest

from src.port.stock import Stock


def make_fake_yf(last_price):
    """Build a fake yf.Ticker whose fast_info returns the given price."""
    fake = MagicMock()
    fake.fast_info = {"last_price": last_price} if last_price is not None else {}
    return fake

class TestInit:
    def test_rejects_empty_string(self):
        with pytest.raises(ValueError):
            Stock("")
    
    def test_rejects_whitespace(self):
        with pytest.raises(ValueError):
            Stock(" ")
    
    def test_normalize_ticker(self):
        with patch("src.port.stock.yf.Ticker", return_value = make_fake_yf(100.0)):
            s = Stock("   aapl   ")
        assert s.ticker == "AAPL"
    
    
class TestTickerProperty:
    def test_is_read_only(self):
        with patch("src.port.stock.yf.Ticker", return_value = make_fake_yf(100.0)):
            s = Stock("AAPL")
        with pytest.raises(AttributeError):
            s.ticker = "TSLA"
    

class TestPrice:
    def test_returns_fetched_price(self):
        with patch("src.port.stock.yf.Ticker", return_value = make_fake_yf(150.25)):
            s = Stock("AAPL")
            assert s.price == 150.25
    
    def test_caches_after_first_call(self):
        fake = make_fake_yf(150.25)
        with patch("src.port.stock.yf.Ticker", return_value = fake):
            s = Stock("AAPL")
            _ = s.price
            _ = s.price
            _ = s.price
        assert fake.fast_info
    
    def test_raises_when_price_missing(self):
        with patch("src.port.stock.yf.Ticker", return_value = make_fake_yf(None)):
            s = Stock("NATICKER")
            with pytest.raises(ValueError, match = "No price available"):
                _ = s.price

