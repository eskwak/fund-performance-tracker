from datetime import datetime
from src.port.stock import Stock


class Portfolio:
    """Positions, valuation, and history for the fund."""
    def __init__(self, data):
        self.__data = data
        self.__allocations = self.__data.load_allocations()
        self.__committed_value = self.__data.load_committed_value()
        self.__stocks = {t: Stock(t) for t in self.__allocations}
        self.__holdings = self.__data.load_holdings()

    @property
    def committed_value(self) -> float:
        return self.__committed_value

    @property
    def current_value(self) -> float:
        if not self.__holdings:
            raise RuntimeError("There are no holdings... Run rebalance()")
        return sum(shares * self.__stocks[t].price for t, shares in self.__holdings.items())

    @property
    def gain_pct(self) -> float:
        return (self.current_value - self.__committed_value) / self.__committed_value

    def rebalance(self) -> None:
        self.__holdings = {
            t: (self.__committed_value * pct) / self.__stocks[t].price
            for t, pct in self.__allocations.items()
        }
        self.__data.save_holdings(self.__holdings)

    def record(self) -> None:
        self.__data.append_history(
            timestamp=datetime.now().isoformat(timespec="seconds"),
            total_value=self.current_value,
            gain_pct=self.gain_pct,
        )

    def __repr__(self) -> str:
        return f"Portfolio(tickers={list(self.__allocations)})"
