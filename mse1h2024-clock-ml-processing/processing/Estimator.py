# import requirements
import cv2
import numpy as np

# import project modules
from ClockCircleExtractor import ClockCircleExtractor
from ClockHandsExtractor import ClockHandsExtractor
from ClockDigitsExtractor import ClockDigitsExtractor


'''
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
        // контур числа не находится на расстоянии от центра меньшем, чем 1/3 от радиуса циферблата
    Круг - должен быть
    Стрелки - опционально
6 - Все числа расположены корректно; начиная с 6 баллов, предъявляются требования только к стрелкам
    Числа - все расположены на своих местах, внутри круга
    Круг - должен быть
    Стрелки - стрелок нет 
        // Вопрос: как отличать 6 баллов от 7 баллов на основании стрелок.
7 - Все числа расположены корректно; время показывается неправильно (сильная погрешность в угле наклона)
    Числа - все расположены на своих местах
    Круг - должен быть
    Стрелки - должны быть; угол наклона сильно отличается от нужного
        // отличие по градусам больше, чем ~60
8 - Все числа расположены корректно; время показывается неправильно (средняя погрешность в угле наклона)
    Числа - должны быть все внутри циферблата по окружности
    Круг - должен быть
    Стрелки - должны быть; угол наклона отличается более чем на ~час-два часа
        // ~31-60 градусов 
9 - Все числа расположены корректно; время показывается неправильно (легкая погрешность в угле наклона)
    Числа - должны быть все внутри циферблата по окружности
    Круг - должен быть
    Стрелки - должны быть; угол наклона отличается в пределах ~(получас; час)
        // ~16-30 градусов
10 - Все числа расположены корректно; время показывается правильно (с допустимой маленькой погрешностью (легчайшая погрешность) в угле наклона)
    Числа - должны быть все внутри циферблата по окружности
    Круг - должен быть
    Стрелки - должны быть; угол наклона точен в пределах ~ получаса;
        // Пусть получас = ~15 градусов
'''

class Estimator:
    """__summary__"""

    def __init__(self) -> None:
        self.__clock_circle_extrator = ClockCircleExtractor()
        self.__clock_hands_extractor = ClockHandsExtractor()
        self.__clock_digits_extractor = ClockDigitsExtractor()
        
    def estimate(self, image: np.array, time: int = 0) -> int:
        estimation_result = 0
        
        digits = self.__clock_digits_extractor.extract(image)
        self.__clock_digits_extractor.show_recognition(image, digits)
        bound = self.__clock_digits_extractor.extract_boundaries(image)
        self.__clock_digits_extractor.show_without_digits(image, bound)

        circle = self.__clock_circle_extrator.extract(image) 
        center = circle[0:2]
        radius = circle[2]
    
        self.__clock_circle_extrator.show_circles(image, [circle])
        hands = self.__clock_hands_extractor.extract(image, circle[0:2], circle[2])
        
        print(f"Digits = {digits}")
        print(f"Circle = {circle}")
        print(f"Hands = {hands}")

        # 1 балл - Нет чисел (нарисовали все что угодно, но не числа (хотя бы одно)):
        if digits is None:
            estimation_result = 1

        if circle is not None:
            digits_count = len(digits) 
            digits_in_circle = self.__digits_in_circle(digits, center, radius)
            digits_in_circle_count = len(digits_in_circle)
            digits_around_circumference = self.__digits_around_circumference(digits, center, radius)
            digits_around_circumference_count = len(digits_around_circumference)

            # 2 балл - Есть числа, но не все (мало (< 6)); круг обязателен; стрелки по желанию =)
            if digits_count < 6:
                estimation_result = 2

            # 3 балл - Количество чисел более 6 и все вне круга;
            if digits_count >= 6 and digits_in_circle_count < len(digits) - 6:
                #self.__clock_digits_extractor.show_recognition(image, self.__digits_in_circle(digits, center, radius))
                estimation_result = 3

            # 4 балл - Количество чисел более 9, в круге более 6 чисел
            if (digits_count >= 9 and digits_in_circle_count == digits_count) or \
                (digits_count >= 11 and digits_in_circle_count >= digits_count/2):
                #self.__clock_digits_extractor.show_recognition(image, self.__digits_in_circle(digits, center, radius))
                estimation_result = 4
            
            # 5 балл - Числа все внутри циферблата по окружности
            if digits_count >= 11 and digits_in_circle_count >= 11 and digits_around_circumference_count >= 11:
                estimation_result = 5

            # 6 балл - 

        #print(self.__digits_in_circle(digits, [circle[0], circle[1]], circle[2]))
        return estimation_result
    
    def __digits_in_circle(self, digits, center, radius):
        is_in_circle = lambda point: radius > np.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2)
        in_circle = []
        for digit in digits:
            digit_box = digit[0]
            if len(list(filter(is_in_circle, digit_box))) > 0:
                in_circle.append(digit)
        
        return in_circle

    def __digits_around_circumference(self, digits, center, radius):
        is_around_circumference = lambda point: radius/3 <= np.sqrt((point[0] - center[0])**2 + (point[1] - center[1])**2)
        around_circumference = []
        for digit in digits:
            digit_box = digit[0]
            if len(list(filter(is_around_circumference, digit_box))) > 0:
                around_circumference.append(digit)
        
        return around_circumference
    
if __name__ == '__main__':
    estimator = Estimator()
    image = cv2.imread("./images/t1_circles.png")
    
    estimation_result = estimator.estimate(image)
    print(f"Esimation result is equal {estimation_result}")