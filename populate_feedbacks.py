import io
import random
from typing import Tuple, Dict

import requests

_letters = [chr(n) for n in range(ord('a'), ord('z') + 1)]


# def generate_random_word(min_k: int = 3, max_k: int = 7) -> str:
#     k = random.randint(min_k, max_k)
#     return ''.join(random.choices(_letters, k=k))


def create_feedback() -> Tuple[Dict, io.StringIO]:
    return dict(
        feedback=' ',
    ), io.StringIO('\n'.join(''))  # ~ 3MB file


if __name__ == '__main__':
    for _ in range(10):
        data, log_file = create_feedback()
        requests.post('http://0.0.0.0:8888/add', data=data, files={'log': log_file})
