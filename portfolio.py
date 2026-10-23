import requests

API_KEY = "" ## Would come from the environment
class Stock:
    name: str

    def current_price(self, live_price: float):
        """
        API call to web service that returns a live price of stock by name.
        API Keys would need to be configured
        """
        if live_price:
            return live_price
        url = f"https://apiservice.com/{self.name}"
        headers = {"Authorization": API_KEY}
        r = requests.get(url, headers)
        return r
    
class Portfolio:
    """
    I added helper functions to make the class more versatile and easier to interact with
    Some of it could be abstracted but it works for this
    """
    def __init__(self) -> None:
        self.stocks = {}
        self.allocation = {}
        self.quantities = {}

    def add_stock(self, stock: Stock, quantity: float):
        self.stocks[stock.name] = stock
        self.quantities[stock.name] = self.quantities.get(stock.name, 0) + quantity

    def set_allocation(self, target_allocations: dict):
        self.allocation = target_allocations

    def portfolio_value(self):
        total = 0.0
        for name, quantity in self.quantities.items():
            price = self.stocks[name].current_price(dummy_data[name])
            total += quantity * price
        return total

    def allocations(self):
        total = self.total_value()

        allocated_portfolio = {}
        for name, quantity in self.quantities.items():
            price = self.stocks[name].current_price(dummy_data[name])
            allocated_portfolio[name] = (quantity * price) / total

        return allocated_portfolio

    def rebalance(self):
        total = self.portfolio_value()
        rebalance_trades = {}
        for name, allocated_weight in self.allocation.items():
            price = self.stocks[name].current_price(dummy_data[name])
            current_quantity = self.quantites.get(name, 0.0)
            current_value = current_quantity * price
            target_value = total * allocated_weight
            ## Postive value will buy shares, negative will sell
            rebalance_trades[name] = (target_value - current_value) / price

        for name, change in rebalance_trades.items():
            self.quantities[name] = self.quantities.get(name, 0.0) + change

        return rebalance_trades
    
dummy_data = {
    "META": 500.0,
    "AAPL": 532.13
}

portfolio = Portfolio()
portfolio.add_stock(stock=Stock("META"), quantity=100)
portfolio.add_stock(stock=Stock("AAPL"), quantity=321)

portfolio.set_allocation({"META": 40, "AAPL": 60})
print("Before Rebalance")
print(f"Total Value: {portfolio.portfolio_value()}")
print(f"Allocations: {portfolio.allocation()}")
print(f"Rebalance Trades: {portfolio.rebalance()}")
print("After Rebalance")
print(f"Total Value: {portfolio.portfolio_value()}")
print(f"Allocations: {portfolio.allocation()}")
