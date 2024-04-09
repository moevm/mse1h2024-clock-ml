# import requirements
import cv2
import numpy as np

# import project modules
from processing.ClockCircleExtractor import ClockCircleExtractor
from processing.ClockHandsExtractor import ClockHandsExtractor
from processing.ClockDigitsExtractor import ClockDigitsExtractor
from processing.const import *


"""
1 - Нет чисел (нарисовали все что угодно, но не числа (хотя бы одно)):
    Числа - нет чисел
    Круг - опционально
    Стрелки - опционально
2 - Есть числа, но не все (мало (< 6)); круг обязателен; стрелки по желанию =)
    Числа - менее 6
    Круг - должен быть
    Стрелки - опционально
3 - Есть числа; все вне круга;
    Числа - более 6 и контур всех вне круга
    Круг - должен быть
    Стрелки - опционально
4 - Есть числа, почти все (в пределах [9-12]); большая часть чисел в круге (в круге как минимум 6 чисел и больше)
    Числа - 
        не менее 9 и все в круге 
        ИЛИ
        не менее 11 и не более 50% вне круга
    Круг - должен быть
    Стрелки - опционально
5 - 
    Числа - должны быть все внутри циферблата по окружности
        /контур числа не находится на расстоянии от центра меньшем, чем 1/3 от радиуса циферблата
    Круг - должен быть
    Стрелки - опционально
6 - Все числа расположены корректно; начиная с 6 баллов, предъявляются требования только к стрелкам
    Числа - все расположены на своих местах, внутри круга
    Круг - должен быть
    Стрелки - стрелок нет 
        /испытуемый обвел цифры кружками, стрелки не учитываются
7 - Все числа расположены корректно; время показывается неправильно (сильная погрешность в угле наклона)
    Числа - все расположены на своих местах
    Круг - должен быть
    Стрелки - должны быть; угол наклона сильно отличается от нужного
        /более 30 градусов, стрелки не учитываются
8 - Все числа расположены корректно; время показывается неправильно (средняя погрешность в угле наклона)
    Числа - должны быть все внутри циферблата по окружности
    Круг - должен быть
    Стрелки - должны быть; угол наклона отличается более чем на ~час-два часа
        /16-30 градусов на часовой и минутной стрелке
9 - Все числа расположены корректно; время показывается неправильно (легкая погрешность в угле наклона)
    Числа - должны быть все внутри циферблата по окружности
    Круг - должен быть
    Стрелки - должны быть; угол наклона отличается в пределах ~(получас; час)
        /~7-15 градусов
        /0-15 градусов на часовой, 16-30 на минутной
10 - Все числа расположены корректно; время показывается правильно (с допустимой маленькой погрешностью (легчайшая погрешность) в угле наклона)
    Числа - должны быть все внутри циферблата по окружности
    Круг - должен быть
    Стрелки - должны быть; угол наклона точен в пределах ~ 0-15 градусов на часовой и минутной стрелке;
        /0-15 градусов на часовой и минутной стрелке
"""


class Estimator:
    """__summary__"""

    def __init__(self) -> None:
        self.__clock_circle_extrator = ClockCircleExtractor()
        self.__clock_hands_extractor = ClockHandsExtractor()
        self.__clock_digits_extractor = ClockDigitsExtractor()
        self.__extracted_digits_angles = {}
        self.__clock_hands_angles = {
            "hour": 0,
            "minute": 0,
        }
        self.__time = {
            "hour": 11,
            "minute": 1,
        }  # TODO: read and parse time from backend

    def estimate(self, image: np.array, time: int = 0) -> int:
        """_summary_

        Args:
            image (np.array): _description_
            time (int, optional): _description_. Defaults to 0.

        Returns:
            int: _description_
        """

        estimation_result = 0

        digits = self.__clock_digits_extractor.extract(image)
        circle = self.__clock_circle_extrator.extract(image)
        # # uncomment for logging
        # self.__clock_digits_extractor.show_recognition(image, digits)

        if circle is not None:
            # # uncomment for logging
            # self.__clock_circle_extrator.show_circles(image, [circle])
            center = circle[0:2]
            radius = circle[2]
            hands = self.__clock_hands_extractor.extract(image, circle[0:2], circle[2])
            self.__define_clock_hands_angle(hands, center)

            # # uncomment for logging
            # self.__clock_hands_extractor.show_lines(image, hands)

        # 1 балл - Нет чисел (нарисовали все что угодно, но не числа (хотя бы одно)):
        if digits is None:
            estimation_result = 1

        if circle is not None:
            digits_count = len(digits)
            digits_in_circle = self.__digits_in_circle(digits, center, radius)
            digits_in_circle_count = len(digits_in_circle)
            digits_around_circumference = self.__digits_around_circumference(
                digits, center, radius
            )
            digits_around_circumference_count = len(digits_around_circumference)

            # 2 балл - Есть числа, но не все (мало (< 6)); круг обязателен; стрелки по желанию =)
            if digits_count < 6:
                estimation_result = 2

            # 3 балл - Количество чисел более 6 и все вне круга;
            if digits_count >= 6 and digits_in_circle_count < len(digits) - 6:
                # self.__clock_digits_extractor.show_recognition(image, self.__digits_in_circle(digits, center, radius))
                estimation_result = 3

            # 4 балл - Количество чисел более 9, в круге более 6 чисел
            if (digits_count >= 9 and digits_in_circle_count == digits_count) or (
                digits_count >= 11 and digits_in_circle_count >= digits_count / 2
            ):
                # self.__clock_digits_extractor.show_recognition(image, self.__digits_in_circle(digits, center, radius))
                estimation_result = 4

            # 5 балл - Числа все внутри циферблата по окружности
            if (
                digits_count >= 11
                and digits_in_circle_count >= 11
                and digits_around_circumference_count >= 11
            ):
                estimation_result = 5

                # 6 балл - числа на своих местах
                self.__define_digits_angle(digits, center)
                if self.__is_all_number_positions_correct():
                    estimation_result = 6
                    if hands is not None and len(hands) == 2:
                        # 10 баллов - стрелки с погрешностью 0-15 градусов
                        if self.__check_time(15, 15):
                            estimation_result = 10
                        # 9 баллов - стрелки с погрешностью 0-15 градусов на часовой, 16-30 на минутной
                        elif self.__check_time(15, 30):
                            estimation_result = 9
                        # 8 баллов - стрелки с погрешностью 16-30
                        elif self.__check_time(30, 30):
                            estimation_result = 8
                        # 7 баллов - стрелки с погрешностью 30+
                        else:
                            estimation_result = 7

        return estimation_result

    def __check_time(self, delta_angle_hour: int, delta_angle_minute: int) -> bool:
        """_summary_

        Args:
            delta_angle_hour (int): _description_
            delta_angle_minute (int): _description_

        Returns:
            bool: _description_
        """

        minute = self.__time["minute"]
        hour = self.__time["hour"]

        if (
            hour in self.__extracted_digits_angles
            and minute in self.__extracted_digits_angles
        ):
            # Нашли оба числа
            hour_angle = self.__extracted_digits_angles[hour]
            minute_angle = self.__extracted_digits_angles[minute]
            return CHECK_ANGLE(
                hour_angle, delta_angle_hour, self.__clock_hands_angles["hour"]
            ) and CHECK_ANGLE(
                minute_angle, delta_angle_minute, self.__clock_hands_angles["minute"]
            )
        elif hour in self.__extracted_digits_angles:
            # Нашли только часовое число
            hour_angle = self.__extracted_digits_angles[hour]
            return CHECK_ANGLE(
                hour_angle, delta_angle_hour, self.__clock_hands_angles["hour"]
            )
        elif minute in self.__extracted_digits_angles:
            # Только минутная
            minute_angle = self.__extracted_digits_angles[minute]
            return CHECK_ANGLE(
                minute_angle, delta_angle_minute, self.__clock_hands_angles["minute"]
            )
        else:
            # Ни одна из стрелок
            return False

    def __digits_in_circle(self, digits, center, radius):
        is_in_circle = lambda point: radius > np.sqrt(
            (point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2
        )
        in_circle = []
        for digit in digits:
            digit_box = digit[0]
            if len(list(filter(is_in_circle, digit_box))) > 0:
                in_circle.append(digit)

        return in_circle

    def __digits_around_circumference(self, digits, center, radius):
        is_around_circumference = lambda point: radius / 3 <= np.sqrt(
            (point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2
        )
        around_circumference = []
        for digit in digits:
            digit_box = digit[0]
            if len(list(filter(is_around_circumference, digit_box))) > 0:
                around_circumference.append(digit)

        return around_circumference

    def __define_digits_angle(self, digits, center):
        for digit in digits:
            digit_number = int(digit[1])
            ([x1, y1], [x2, y2], [x3, y3], [x4, y4]) = digit[0]
            digit_center = ((x1 + x2) / 2, (y1 + y3) / 2)

            dx = digit_center[0] - center[0]
            dy = digit_center[1] - center[1]
            angle = np.arctan2(dx, -dy)
            angle_degrees = np.round(np.degrees(angle), 3)
            if angle_degrees < 0:
                angle_degrees += 360.0

            self.__extracted_digits_angles[digit_number] = angle_degrees

    def __define_clock_hands_angle(self, clock_hands, center):
        # [(x1, y1, x2, y2)]
        hands = []
        for clock_hand in clock_hands:
            (x1, y1, x2, y2) = clock_hand
            x_start, x_end = (
                (x1, x2) if abs(center[0] - x1) < abs(center[0] - x2) else (x2, x1)
            )
            y_start, y_end = (
                (y1, y2) if abs(center[1] - y1) < abs(center[1] - y2) else (y2, y1)
            )
            dx = x_end - x_start
            dy = y_end - y_start
            clock_hand_length = np.sqrt(dx**2 + dy**2)

            angle = np.arctan2(dx, -dy)
            angle_degrees = np.round(np.degrees(angle), 3)
            if angle_degrees < 0:
                angle_degrees += 360.0
            hands.append((clock_hand_length, angle_degrees))

        hands = sorted(hands, key=lambda elem: elem[0])
        self.__clock_hands_angles["hour"] = hands[0][1]
        self.__clock_hands_angles["minute"] = hands[1][1]

    def __parse_time(self):
        # TODO: parsing time
        pass

    def __is_all_number_positions_correct(self) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        for digit, angle in self.__extracted_digits_angles.items():
            if digit in REFERENCE_DIGITS_ANGLES:
                if not CHECK_ANGLE(
                    REFERENCE_DIGITS_ANGLES[digit], DELTA_DIGIT_ANGLE, angle
                ):
                    return False
        return True


if __name__ == "__main__":
    estimator = Estimator()
    image = cv2.imread("./images/t1_circles.png")

    estimation_result = estimator.estimate(image)
    print(f"Esimation result is equal {estimation_result}")
