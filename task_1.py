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
import random
from collections import deque


class SlidingWindowRateLimiter:
    """
    Rate Limiter with Sliding Window
    """

    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        self.messages = deque()

    def _clean_window(self):
        """Clean window"""
        while (
            self.messages and self.messages[0]["time"] < time.time() - self.window_size
        ):
            self.messages.popleft()

    def can_send_message(self, user_id: str) -> bool:
        """Check that user can send message"""
        self._clean_window()
        user_messages = self._get_user_messages(user_id)
        return len(user_messages) < self.max_requests

    def record_message(self, user_id: str):
        """Record message to chat"""
        if self.can_send_message(user_id):
            self.messages.append({"user_id": user_id, "time": time.time()})
            self._clean_window()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> int:
        """Return time until next allowed message"""
        self._clean_window()
        user_messages = self._get_user_messages(user_id)
        if not user_messages:
            return 0
        return self.window_size - (time.time() - user_messages[-1]["time"])

    def _get_user_messages(self, user_id: str) -> list:
        """Return messages"""
        return [message for message in self.messages if message["user_id"] == user_id]


def test_rate_limiter():
    """Test rate limiter"""
    # Створюємо rate limiter: вікно 10 секунд, 1 повідомлення
    green_color = "\033[92m"  # Green
    red_color = "\033[91m"  # Red
    reset_color = "\033[0m"  # Reset
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Симулюємо потік повідомлень від користувачів (послідовні ID від 1 до 20)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, 11):
        # Симулюємо різних користувачів (ID від 1 до 5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(
            f"Повідомлення {message_id:2d} | Користувач {user_id} | ",
            (
                f"{green_color}✓{reset_color}"
                if result
                else f"{red_color}× (очікування {wait_time:.1f}с){reset_color}"
            ),
        )

        # Невелика затримка між повідомленнями для реалістичності
        # Випадкова затримка від 0.1 до 1.0 секунди
        time.sleep(random.uniform(0.1, 1.0))

    # Чекаємо, поки вікно очиститься
    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(
            f"Повідомлення {message_id:2d} | Користувач {user_id} | ",
            (
                f"{green_color}✓{reset_color}"
                if result
                else f"{red_color}× (очікування {wait_time:.1f}с){reset_color}"
            ),
        )
        # Випадкова затримка від 0.1 до 1.0 секунди
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()
