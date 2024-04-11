# import requirements
import numpy as np
from typing import Union


class ClockCircle:
    def __init__(
        self, center_coordinates: Union[tuple, list, np.ndarray], radius: int
    ) -> None:
        self._center_coordinates = (center_coordinates[0], center_coordinates[1])
        self._radius = radius

    @property
    def center_coordinates(self) -> tuple[int, int]:
        return self._center_coordinates

    @property
    def radius(self) -> int:
        return self._radius


class ClockHands:
    def __init__(self) -> None:
        pass


class ClockDigits:
    def __init__(self) -> None:
        pass


if __name__ == "__main__":
    circle = ClockCircle(center_coordinates=[1, 2], radius=5)
    print(circle.center_coordinates, circle.radius)
