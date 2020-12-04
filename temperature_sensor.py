# TsicInputChannel and ZacWireInputChannel require pigpio
# for GPIO access with precise timing:
import threading
import time

import pigpio
from tsic import TsicInputChannel, TSIC306, Measurement


class TemperatureSimulator(object):

    def __init__(self, target) -> None:
        self._target = target
        self._current_time = 0
        self._prev_temperature = 0

    def get(self, force) -> float:
        temp = self._prev_temperature + force / 20.0
        self._prev_temperature = temp
        return temp

    def set(self, temperature):
        self._prev_temperature = temperature


class TemperatureReader(object):

    def __init__(self, gpio=4):
        self._temperature: float = 0
        self._lock = threading.Lock()
        pi = pigpio.pi()
        self.tsic = TsicInputChannel(pigpio_pi=pi, gpio=gpio, tsic_type=TSIC306)
        self.tsic.start(self._store_measurement)
        time.sleep(0.2)

    def get(self) -> float:
        self._lock.acquire()
        ret_temp = self._temperature
        self._lock.release()
        return ret_temp

    def close(self):
        self.tsic.stop()

    def _store_measurement(self, measurement: Measurement):
        self._lock.acquire()
        self._temperature = round(measurement.degree_celsius)
        self._lock.release()


simulator = TemperatureSimulator(105)
#temp_reader = TemperatureReader()