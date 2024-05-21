# import requirements
import numpy as np
from typing import Union


class ClockCircle:
    """Class for keeping the information about clock circle"""
    
    def __init__(
        self, center_coordinates: Union[tuple, list, np.ndarray], radius: int
    ) -> None:
        """Initialization the ClockCircle"""

        self._center_coordinates = (center_coordinates[0], center_coordinates[1])
        self._radius = radius

    @property
    def center_coordinates(self) -> tuple[int, int]:
        """This is a method that returns the center point of the dial

        Returns:
            tuple[int, int]: point of circle center
        """
        return self._center_coordinates

    @property
    def radius(self) -> int:
        """This is a method that returns the radius of the dial

        Returns:
            int: radius value
        """
        return self._radius

    def __str__(self) -> str:
        return (
            f"Center coordinates = {self._center_coordinates}"
            + "\n"
            + f"Radius = {self._radius}"
        )


class ClockHands:
    def __init__(self, lines: list[tuple[int, int, int, int]]) -> None:
        self._clock_hands = lines.copy()
        self._angles = {"hour": 0, "minute": 0}

    @property
    def clock_hands(self):
        return self._clock_hands

    def get_clock_hands_count(self) -> int:
        if self._clock_hands:
            return len(self._clock_hands)
        return 0

    @property
    def hour_angle(self):
        return self._angles["hour"]

    @property
    def minute_angle(self):
        return self._angles["minute"]

    def define_angle(self, clock_center: list[int, int]) -> None:
        hands_description = []  # (длина стрелки, угол стрелки)
        for clock_hand in self._clock_hands:
            (x1, y1, x2, y2) = clock_hand
            x_start, x_end = (
                (x1, x2)
                if abs(clock_center[0] - x1) < abs(clock_center[0] - x2)
                else (x2, x1)
            )
            y_start, y_end = (
                (y1, y2)
                if abs(clock_center[1] - y1) < abs(clock_center[1] - y2)
                else (y2, y1)
            )
            dx = x_end - x_start
            dy = y_end - y_start
            clock_hand_length = np.sqrt(dx**2 + dy**2)

            angle = np.arctan2(dx, -dy)
            angle_degrees = np.round(np.degrees(angle), 3)
            if angle_degrees < 0:
                angle_degrees += 360.0
            hands_description.append((clock_hand_length, angle_degrees))

        hands_description = sorted(hands_description, key=lambda elem: elem[0])
        self._angles["hour"] = hands_description[0][1]
        self._angles["minute"] = hands_description[1][1]

    def __str__(self) -> str:
        return f"First line {self._clock_hands[0]}" + "\n" + f"Second line {self._clock_hands[1]}"


class ClockDigits:
    def __init__(
        self,
        digits: list[
            tuple[
                list[list[int, int], list[int, int], list[int, int], list[int, int]],
                str,
                int,
            ]
        ],
    ) -> None:
        self._digits = digits.copy()
        self._angles = {}

    @property
    def angles(self) -> dict:
        return self._angles.copy()

    def get_digit_angle(self, digit: int) -> float:
        return self._angles.get(digit)

    @property
    def digits(
        self,
    ) -> list[
        tuple[
            list[list[int, int], list[int, int], list[int, int], list[int, int]],
            str,
            int,
        ]
    ]:
        "The boundaries is represented by a list in the following format: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]"

        return self._digits.copy()

    def define_angle(self, center: list[int, int]) -> None:
        for digit in self._digits:
            digit_number = int(digit[1])
            ([x1, y1], [x2, y2], [x3, y3], [x4, y4]) = digit[0]
            digit_center = ((x1 + x2) / 2, (y1 + y3) / 2)

            dx = digit_center[0] - center[0]
            dy = digit_center[1] - center[1]
            angle = np.arctan2(dx, -dy)
            angle_degrees = np.round(np.degrees(angle), 3)
            if angle_degrees < 0:
                angle_degrees += 360.0

            self._angles[digit_number] = angle_degrees

    def __str__(self) -> str:
        digit_list = [digit[1] for digit in self._digits]
        return f"digits = {digit_list}"
