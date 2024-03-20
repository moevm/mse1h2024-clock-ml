# import requirements
import cv2
import numpy as np

# import project modules
from ClockCircleExtractor import ClockCircleExtractor
from ClockHandsExtractor import ClockHandsExtractor
from ClockDigitsExtractor import ClockDigitsExtractor


class Estimator:
    """__summary__"""

    def __init__(self) -> None:
        self.__clock_circle_extrator = ClockCircleExtractor()
        self.__clock_hands_extractor = ClockHandsExtractor()
        self.__clock_digits_extractor = ClockDigitsExtractor()
        
    def estimate(self, image: np.array, time: int = 0) -> int:
        estimation_result = 0
        
        digits = self.__clock_digits_extractor.extract(image)
        circle = self.__clock_circle_extrator.extract(image) 
        hands = self.__clock_hands_extractor.extract(image, circle[0:2], circle[2])
        
        print(f"Digits = {digits}")
        print(f"Circle = {circle}")
        print(f"Hands = {hands}")

        if digits is None:
            estimation_result = 1
        
        return estimation_result
    
    
if __name__ == '__main__':
    estimator = Estimator()
    image = cv2.imread("./images/circle.png")
    
    estimation_result = estimator.estimate(image)
    print(f"Esimation result is equal {estimation_result}")