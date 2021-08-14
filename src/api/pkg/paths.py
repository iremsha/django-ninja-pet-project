import random


def get_individual_path(instance, filename):
    return str(random.getrandbits(32)) + filename
