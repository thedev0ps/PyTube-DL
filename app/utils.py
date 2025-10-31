import time


def type_out(string: str, delay: float = 0.1):
    """
    Prints a string one character at a time, simulating typing.

    Args:
        string (str): The text to be printed.
        delay (float, optional): Time delay between characters in seconds. Defaults to 0.1.
    """
    for char in string:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()
