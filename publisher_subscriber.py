from abc import ABC, abstractmethod

# Observer Interface
class IObserver(ABC):
    @abstractmethod
    def notify(self, data: object):
        pass

# Observable interface
class IObservable(ABC):
    @abstractmethod
    def register(self, observer: IObserver):
        pass
    
    @abstractmethod
    def unregister(self, observer: IObserver):
        pass
    
    @abstractmethod
    def notify_observers(self, data: object):
        pass

# Implement observable helper class
class ObservableImpl(IObservable):
    def __init__(self):
        self._obj_container = {}

    def register(self, observer: IObserver):
        self._obj_container[observer] = None

    def unregister(self, observer: IObserver):
        del self._obj_container[observer]

    def notify_observers(self, data: object):
        for observer in self._obj_container.keys():
            observer.notify(data)

# Implement Stock class as subject
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

# Implement observer (subscriber) class
class StockDisplay(IObserver):
    def notify(self, data: object):
        print(f"Current ask price: {data}")
