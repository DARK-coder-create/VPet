from PySide6.QtCore import QTimer


class GlobalTimer:
    _instance = None
    _timer = None
    _subscribers = []
    _last_time = 0
    _delta_time = 0
    _ticks_per_second = 60

    def __new__(cls, ticks_per_second=60):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._ticks_per_second = ticks_per_second
            cls._timer = QTimer()
            cls._last_time = cls._timer.remainingTime()
            cls._timer.timeout.connect(cls._update_all)
            print(ticks_per_second)
            interval = int(1000 / ticks_per_second)
            cls._timer.start(interval)
        return cls._instance

    @classmethod
    def _update_all(cls):
        current_time = cls._timer.remainingTime()
        cls._delta_time = (current_time - cls._last_time) / 1000.0
        cls._last_time = current_time

        for subscriber in cls._subscribers:
            if hasattr(subscriber, 'global_update'):
                subscriber.global_update(cls._delta_time)

    @classmethod
    def get_delta_time(cls):
        return cls._delta_time

    @classmethod
    def get_ticks_per_second(cls):
        return cls._ticks_per_second

    @classmethod
    def set_ticks_per_second(cls, ticks_per_second):
        cls._ticks_per_second = ticks_per_second
        interval = int(1000 / ticks_per_second)
        if cls._timer:
            cls._timer.setInterval(interval)

    @classmethod
    def subscribe(cls, subscriber):
        if subscriber not in cls._subscribers:
            cls._subscribers.append(subscriber)

    @classmethod
    def unsubscribe(cls, subscriber):
        if subscriber in cls._subscribers:
            cls._subscribers.remove(subscriber)

    @classmethod
    def stop(cls):
        if cls._timer:
            cls._timer.stop()

    @classmethod
    def start(cls, interval=None):
        if cls._timer:
            if interval is None:
                interval = int(1000 / cls._ticks_per_second)
            cls._timer.start(interval)