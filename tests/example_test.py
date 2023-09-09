def add(x: int, y: int) -> int:
    return x + y


def test_add() -> None:
    assert add(1, 2) == 3
    assert add(2, 2) == 4
