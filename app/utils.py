import time


def type_out(string: str, delay: float = 0.1):
    for char in string:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
