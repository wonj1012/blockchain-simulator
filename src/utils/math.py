import random


def adjust_random_percent(prev_percent: float, max_percent: float, change_limit: float):
    random_percent = random.uniform(-1 * max_percent, max_percent)
    return max(
        min(random_percent, prev_percent + change_limit), prev_percent - change_limit
    )
