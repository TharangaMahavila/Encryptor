def secret_to_shift(secret):
    return sum(ord(c) for c in secret) % 26
