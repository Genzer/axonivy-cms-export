import sys
from typing import Sequence, TypeVar, Union

number = Union[int, float, complex]
V = TypeVar("V")
T = TypeVar("T", Sequence[V], number)


def double(com: T) -> T:
    return com * 2


def main():
    print("Sequence doubling", double(sys.argv))
    print("Each arg doubling", [double(arg) for arg in sys.argv])
    raise Exception("This project is not started!!")


if __name__ == "__main__":
    main()
