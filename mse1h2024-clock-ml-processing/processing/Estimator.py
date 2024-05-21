# import requirements
import numpy as np

# import project modules
from processing.extractors.ClockCircleExtractor import ClockCircleExtractor
from processing.extractors.ClockHandsExtractor import ClockHandsExtractor
from processing.extractors.ClockDigitsExtractor import ClockDigitsExtractor
from processing.const.const import *
from processing.objects.objects import *


class Estimator:
    """__summary__"""

    def __init__(self) -> None:
        self.__clock_circle_extrator = ClockCircleExtractor()
        self.__clock_hands_extractor = ClockHandsExtractor()
        self.__clock_digits_extractor = ClockDigitsExtractor()
        self.__time = {
            "hour": 11,
            "minute": 1,
        }

    def __parse_time(self, time: tuple[int, int]) -> None:
        self.__time["hour"] = time[0]
        self.__time["minute"] = 12 if time[1] == 0 else time[1] // 5

    def estimate(self, image: np.array, time: tuple[int, int]) -> int:
        """_summary_

        Args:
            image (np.array): _description_
            time (int, optional): _description_. Defaults to 0.

        Returns:
            int: _description_
        """

        self.__parse_time(time)

        estimation_result = 1

        digits = self.__clock_digits_extractor.extract(image)
        circle = self.__clock_circle_extrator.extract(image)
        # # uncomment for logging
        # self.__clock_digits_extractor.show_recognition(image, digits)

        if circle is not None:
            # # uncomment for logging
            # self.__clock_circle_extrator.show_circles(image, [circle])
            clock_center = circle.center_coordinates
            clock_radius = circle.radius
            hands = self.__clock_hands_extractor.extract(
                image, clock_center, clock_radius
            )

            if hands is not None:
                hands.define_angle(clock_center)
                # uncomment for logging
                # self.__clock_hands_extractor.show_lines(image, hands)

        # 1 балл - Нет чисел (нарисовали все что угодно, но не числа (хотя бы одно)):
        if circle is not None and digits is not None:
            digits_count = len(digits.digits)
            digits_in_circle = self.__digits_in_circle(digits, circle)
            digits_in_circle_count = len(digits_in_circle)
            digits_around_circumference = self.__digits_around_circumference(
                digits, circle
            )
            digits_around_circumference_count = len(digits_around_circumference)

            # 2 балл - Есть числа, но не все (мало (< 6) ограничивается в 3х баллах); круг обязателен; стрелки по желанию =)
            if digits_count > 0:
                estimation_result = 2

            # 3 балл - Количество чисел более 6 и все вне круга;
            if digits_count >= 6 and digits_in_circle_count == 0:
                # self.__clock_digits_extractor.show_recognition(image, self.__digits_in_circle(digits, center, clock_radius))
                estimation_result = 3

            # 4 балл - Количество чисел более 9, в круге более 6 чисел
            if (digits_count >= 9 and digits_in_circle_count == digits_count) or (
                digits_count >= 11 and digits_in_circle_count >= digits_count / 2
            ):
                # self.__clock_digits_extractor.show_recognition(image, self.__digits_in_circle(digits, center, clock_radius))
                estimation_result = 4

            # 5 балл - Числа все внутри циферблата по окружности
            if (
                digits_count >= 11
                and digits_in_circle_count >= 11
                and digits_around_circumference_count >= 11
            ):
                estimation_result = 5

                # 6 балл - числа на своих местах
                digits.define_angle(clock_center)
                if self.__is_all_number_positions_correct(digits):
                    estimation_result = 6

                    if hands is not None and hands.get_clock_hands_count() == 2:
                        # 10 баллов - стрелки с погрешностью 0-15 градусов
                        if self.__check_time(15, 15, digits, hands):
                            estimation_result = 10
                        # 9 баллов - стрелки с погрешностью 0-15 градусов на часовой, 16-30 на минутной
                        elif self.__check_time(15, 30, digits, hands):
                            estimation_result = 9
                        # 8 баллов - стрелки с погрешностью 16-30
                        elif self.__check_time(30, 30, digits, hands):
                            estimation_result = 8
                        # 7 баллов - стрелки с погрешностью 30+
                        else:
                            estimation_result = 7

        return estimation_result

    def __check_time(
        self,
        delta_angle_hour: int,
        delta_angle_minute: int,
        digits: ClockDigits,
        clock_hands: ClockHands,
    ) -> bool:
        """_summary_

        Args:
            delta_angle_hour (int): _description_
            delta_angle_minute (int): _description_

        Returns:
            bool: _description_
        """

        minute = self.__time["minute"]
        hour = self.__time["hour"]

        if hour in digits.angles and minute in digits.angles:
            # Нашли оба числа
            hour_angle = digits.angles[hour]
            minute_angle = digits.angles[minute]
            return CHECK_ANGLE(
                hour_angle, delta_angle_hour, clock_hands.hour_angle
            ) and CHECK_ANGLE(
                minute_angle, delta_angle_minute, clock_hands.minute_angle
            )
        elif hour in digits.angles:
            # Нашли только часовое число
            hour_angle = digits.angles[hour]
            return CHECK_ANGLE(hour_angle, delta_angle_hour, clock_hands.hour_angle)
        elif minute in digits.angles:
            # Только минутная
            minute_angle = digits.angles[minute]
            return CHECK_ANGLE(
                minute_angle, delta_angle_minute, clock_hands.minute_angle
            )
        else:
            # Ни одна из стрелок
            return False

    def __digits_in_circle(self, digits: ClockDigits, clock_circle: ClockCircle):
        is_in_circle = lambda point: clock_circle.radius > np.sqrt(
            (point[0] - clock_circle.center_coordinates[0]) ** 2
            + (point[1] - clock_circle.center_coordinates[1]) ** 2
        )
        in_circle = []
        for digit in digits.digits:
            digit_box = digit[0]
            if len(list(filter(is_in_circle, digit_box))) > 0:
                in_circle.append(digit)

        return in_circle

    def __digits_around_circumference(
        self, digits: ClockDigits, clock_circle: ClockCircle
    ):
        is_around_circumference = lambda point: clock_circle.radius / 3 <= np.sqrt(
            (point[0] - clock_circle.center_coordinates[0]) ** 2
            + (point[1] - clock_circle.center_coordinates[1]) ** 2
        )
        around_circumference = []
        for digit in digits.digits:
            digit_box = digit[0]
            if len(list(filter(is_around_circumference, digit_box))) > 0:
                around_circumference.append(digit)

        return around_circumference

    def __is_all_number_positions_correct(self, digits: ClockDigits) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        for digit, angle in digits.angles.items():
            if digit in REFERENCE_DIGITS_ANGLES:
                if not CHECK_ANGLE(
                    REFERENCE_DIGITS_ANGLES[digit], DELTA_DIGIT_ANGLE, angle
                ):
                    return False
        return True
