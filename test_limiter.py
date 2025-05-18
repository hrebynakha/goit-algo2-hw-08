"""Test rate limiter"""

import time
import random


def test_rate_limiter(
    limiter,
    users_count: int = 5,
    messages_count: int = 10,
):
    """Test rate limiter"""
    green_color = "\033[92m"  # Green
    red_color = "\033[91m"  # Red
    reset_color = "\033[0m"  # Reset

    # Симулюємо потік повідомлень від користувачів (послідовні ID від 1 до 20)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, messages_count + 1):
        user_id = message_id % users_count + 1

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
    for message_id in range(messages_count + 1, messages_count * 2 + 1):
        user_id = message_id % users_count + 1
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
        time.sleep(random.uniform(0.1, 1.0))
