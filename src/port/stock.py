import yfinance as yf

class Stock:
    """Wrapper over market data for a single ticker.
    """
    def __init__(self, ticker: str):
        if not ticker or not ticker.strip():
            raise ValueError("Ticker must be a non-empty string")
        
        self.__ticker = ticker.strip().upper()
        self.__yf = yf.Ticker(self.__ticker)
        self.__cached_price: float | None = None
        
    @property
    def ticker(self) -> str:
        """Returns the stock's ticker symbol."""
        return self.__ticker
    
    @property
    def price(self) -> float:
        """Returns the stock's last traded price."""
        if self.__cached_price is None:
            self.__cached_price = self.__fetch_price()
        return self.__cached_price
    
    def __fetch_price(self) -> float:
        last_price = self.__yf.fast_info.get("last_price")
        if last_price is None:
            raise ValueError(f"No price available for {self.__ticker!r}")
        return float(last_price)
    
    def __repr__(self) -> str:
        return f"Stock({self.__ticker!r})"