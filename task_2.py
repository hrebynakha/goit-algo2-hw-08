"""
Task 2
Реалізація Rate Limiter з використанням алгоритму Throttling
для обмеження частоти повідомлень у чаті

У чат-системі необхідно реалізувати механізм обмеження частоти
повідомлень від користувачів для запобігання спаму.
Реалізація повинна використовувати алгоритм Throttling для
контролю часових інтервалів між повідомленнями,
який забезпечує фіксований інтервал очікування між
повідомленнями користувача й обмежує частоту відправки,
якщо цього інтервалу не дотримано.

"""

import time
from typing import Dict
from test_limiter import test_rate_limiter


class ThrottlingRateLimiter:
    """
    Rate Limiter with Throttling
    """

    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        self.last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        """Check that user can send message"""
        if user_id not in self.last_message_time:
            return True
        return time.time() - self.last_message_time[user_id] >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        """Record message to chat"""
        if self.can_send_message(user_id):
            self.last_message_time[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """Return time until next allowed message"""
        if user_id not in self.last_message_time:
            return 0.0
        # call max to return 0.0 if time until next allowed message is negative
        return max(
            0.0, self.min_interval - (time.time() - self.last_message_time[user_id])
        )


if __name__ == "__main__":
    limiter = ThrottlingRateLimiter()
    test_rate_limiter(limiter)
