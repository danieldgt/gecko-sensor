import time

class sensor:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self._humidity = None
        self._temperature = None

    def trigger(self):
        self._humidity = None
        self._temperature = None

        h, t = self.pi.read_dht(self.gpio)
        if h is not None and t is not None:
            self._humidity = h
            self._temperature = t

    def humidity(self):
        return self._humidity

    def temperature(self):
        return self._temperature

    def cancel(self):
        pass
