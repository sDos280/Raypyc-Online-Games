import ctypes
import random
import raypyc

class Player:
    def __init__(self, is_x: bool) -> None:
        self.is_x = is_x
        self.my_hash = hash(random.random())
