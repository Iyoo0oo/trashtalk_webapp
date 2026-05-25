import hashlib
from services.storage import read, write

USERS_FILE = "data/users.csv"


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def register(u, p):
    write(USERS_FILE, [u, hash_pw(p)])


def login(u, p):
    users = read(USERS_FILE)
    hashed = hash_pw(p)

    return any(user == u and pw == hashed for user, pw in users)