import csv
import os

DATA = "data"
USERS = f"{DATA}/users.csv"
HISTORY = f"{DATA}/history.csv"
REWARDS = f"{DATA}/rewards.csv"


def init():
    os.makedirs(DATA, exist_ok=True)

    files = {
        USERS: ["user", "pass"],
        HISTORY: ["user", "category", "sub", "weight"],
        REWARDS: ["user", "points"]
    }

    for f, h in files.items():
        if not os.path.exists(f):
            with open(f, "w", newline="") as x:
                csv.writer(x).writerow(h)


def read(file):
    with open(file, "r") as f:
        return list(csv.reader(f))[1:]


def write(file, row):
    with open(file, "a", newline="") as f:
        csv.writer(f).writerow(row)


def update_rewards(user, points):
    data = {}

    try:
        for u, p in read(REWARDS):
            data[u] = int(p)
    except:
        pass

    data[user] = data.get(user, 0) + points

    with open(REWARDS, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["user", "points"])
        for k, v in data.items():
            w.writerow([k, v])