from random import choice, randint
import string


def random_string():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.whitespace
    return ''.join(choice(chars) for _ in range(randint(10, 20)))


def random_number():
    return randint(10, 1000)
