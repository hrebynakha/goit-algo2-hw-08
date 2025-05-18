"""
Реалізація Rate Limiter з використанням алгоритму Sliding Window
для обмеження частоти повідомлень у чаті

У чат-системі необхідно реалізувати механізм обмеження частоти
 повідомлень від користувачів для запобігання спаму.
 Реалізація повинна використовувати алгоритм Sliding Window
 для точного контролю часових інтервалів,
 який дозволяє відстежувати кількість повідомлень
 у заданому часовому вікні й обмежувати користувачів
 у надсиланні повідомлень, якщо ліміт перевищено.

"""

import time
from typing import Deque
from collections import deque
from test_limiter import test_rate_limiter


class SlidingWindowRateLimiter:
    """
    Rate Limiter with Sliding Window
    """

    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.messages: dict[str, Deque[float]] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        """Clean window"""
        if user_id not in self.messages:
            return
        while (
            self.messages[user_id]
            and self.messages[user_id][0] < current_time - self.window_size
        ):
            self.messages[user_id].popleft()

    def can_send_message(self, user_id: str) -> bool:
        """Check that user can send message"""
        self._cleanup_window(user_id, time.time())
        return len(self.messages.get(user_id, [])) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        """Record message to chat"""
        if self.can_send_message(user_id):
            if user_id not in self.messages:
                self.messages[user_id] = deque()
            self.messages[user_id].append(time.time())
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:
        """Return time until next allowed message"""
        if not self.messages.get(user_id):
            return 0.0
        now = time.time()
        self._cleanup_window(user_id, now)
        # call max to return 0.0 if time until next allowed message is negative
        return max(0.0, self.window_size - (now - self.messages[user_id][0]))


if __name__ == "__main__":
    limiter = SlidingWindowRateLimiter()
    test_rate_limiter(limiter)
