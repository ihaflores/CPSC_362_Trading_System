import random
from abc import ABC, abstractmethod

# Observer Interface
class IObserver(ABC):
    @abstractmethod
    def notify(self, data: object):
        pass

# Observable interface 
class IObservable(ABC):
    @abstractmethod
    def notify_observers(self, data: object):
        pass

# Interface helper classegister)
class ObservableImpl(IObservable):
    def __init__(self):
        self._obj_container = []

    def notify_observers(self, data: object):
        for observer in self._obj_container:
            observer.notify(data)

# Stock publisher implements observer pattern
class Stock(ObservableImpl):
    def __init__(self):
        super().__init__()
        self._ask_price = None

    @property
    def ask_price(self):
        return self._ask_price

    @ask_price.setter
    def ask_price(self, value):
        self._ask_price = value
        self.notify_observers(self._ask_price)

    def simulate_price_change(self):
        for _ in range(10):  # Simulate 10 price changes
            random_price = random.uniform(50, 150)  # Generate random price
            self.ask_price = random_price  # Update ask price

# StockDisplay is subscriber in observer pattern
class StockDisplay(IObserver):
    def notify(self, data: object):
        print(f"Current ask price: {data}")