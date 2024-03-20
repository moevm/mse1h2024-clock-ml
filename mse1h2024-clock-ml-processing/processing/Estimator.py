# import requirements
import numpy as np

# import project modules
from ClockCircleExtractor import ClockCircleExtractor
from ClockHandsExtractor import ClockHandsExtractor
from DigitsPositionExtractor import DigitsPositionExtractor


class Estimator:
    """__summary__"""

    def __init__(self) -> None:
        self.__clock_circle_extrator = None
        self.__clock_hands_extractor = None
        self.__digits_position_extractor = None
        
    def estimate(self, image: np.array) -> int:
        
        return 10