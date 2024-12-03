from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    array_copy = array[:]
    if len(array) == 0:
        return 0
    elif number > array[-1]:
        return len(array)
    while True:
        avg = array_copy[len(array_copy) // 2]
        if number > avg and len(array_copy) > 1:
            array_copy = array_copy[len(array_copy) // 2 :]
        elif number < avg and len(array_copy) > 1:
            array_copy = array_copy[: len(array_copy) // 2]
        elif number == avg:
            return array.index(avg)
        elif len(array_copy) == 1 and number > avg:
            return array.index(array[len(array) - array[::-1].index(avg)])
        elif len(array_copy) == 1 and number < avg:
            return array.index(avg)


if __name__ == "__main__":
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
