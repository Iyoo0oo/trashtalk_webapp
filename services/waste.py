from dataclasses import dataclass
from collections import deque
from config import WASTE

queue = deque()
id_counter = 1


@dataclass
class Pickup:
    id: int
    user: str
    address: str
    category: str
    sub: str
    weight: float


def norm(text):
    return text.strip().lower()


def validate(cat, sub):
    cat = norm(cat)
    sub = norm(sub)

    if cat not in WASTE:
        return False

    return sub in WASTE[cat]


def add(user, address, cat, sub, weight):
    global id_counter

    cat = norm(cat)
    sub = norm(sub)

    if not validate(cat, sub):
        return None

    p = Pickup(id_counter, user, address, cat, sub, weight)
    queue.append(p)
    id_counter += 1
    return p


def process():
    if queue:
        return queue.popleft()


def get_all():
    return list(queue)