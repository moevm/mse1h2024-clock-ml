# import requirements
import cv2
import numpy as np


class ClockHandsExtractor:
    """Class for extracting the positions of clock hands from an image."""

    def __init__(self, image: np.array, center: list[int], radius: int) -> None:
        """
        Initialization the ClockHandsExtractor.

        Parameters
        ----------
        image : np.array
            Image object from which numbers are read
        center : list[int]
            Сenter point of the dial or image [x, y]
        radius : int
            Radius of the dial or the maximum circle inscribed in the image
        """

        # Initializing an Image Object
        self.__image = image
        self.__gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Initializing a clock hands list
        self.__clock_hands = list()
        
        # Initializing a basic constants
        self.__center = center
        self.__center_eps = radius/4
        self.__min_clock_hand_length = radius/5
        self.__tilt_coef_eps = 0.05

    def get_extracted(self) -> list[tuple] | None:
        """This method returns a list of recognized clock hands"""

        return self.__clock_hands if self.__clock_hands else None

    def extract(self) -> None:
        """This method extracts clock hands from an image"""

        # Initializing the line detector
        line_segment_detector = cv2.createLineSegmentDetector(
            refine=cv2.LSD_REFINE_STD,
            # sigma_scale=2, # длиннее палки
            # quant=2.0,
            # ang_th = 80, # ideal
            density_th=0.1, # Minimal density of aligned region points in the enclosing rectangle. 
        )

        # Detection of all lines
        lines = line_segment_detector.detect(
            image=self.__gray_image,
        )[0]

        if lines is None:
            print('Not found lines on input image')
            return

        # Selecting lines that are clock hands
        self.__select_clock_hands(lines)

    def __select_clock_hands(self, lines: list[list[tuple[int, int, int, int]]]) -> None:
        """"
        This method selects the lines that are the hands of the clock
        
        Parameters
        ----------
        lines : list[list[tuple[int, int, int, int]]]
            list of lines, among which you need to select the ones responsible for the clock lines.
            The lines is represented by a list in the following format: [(x1, y1, x2, y2)].
        """

        # self.show_lines(self.__image, lines)
        # Initializing set tilt coefficients for recognized clock hands
        tilt_coefs = set()
        
        falls_within = lambda coord, limit, eps: limit - eps <= coord <= limit + eps 
        for line in lines:
            (x1, y1, x2, y2) = line[0]
            tilt_coef = (y2-y1)/(x2-x1)
            if (
                (
                    falls_within(x1, self.__center[0], self.__center_eps)
                    and falls_within(y1, self.__center[1], self.__center_eps)
                )
                or (
                    falls_within(x2, self.__center[0], self.__center_eps)
                    and falls_within(y2, self.__center[1], self.__center_eps)
                )
            ) and np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) >= self.__min_clock_hand_length and \
                not self.__is_exist_tilt_coef(tilt_coef, tilt_coefs):
                
                # Add new line to clock hands
                self.__clock_hands.append((x1, y1, x2, y2))
                # self.show_lines(self.__image, [line])
                
                # Update existing tilt coefficients
                tilt_coefs.add(tilt_coef)

    def __is_exist_tilt_coef(self, tilt_coef: float, tilt_coefs: set[float]) -> bool:
        """This method checks for the presence of a clock hand with the same slope factor"""

        for cur_tilt_coef in tilt_coefs:
            if cur_tilt_coef - self.__tilt_coef_eps <= tilt_coef <= cur_tilt_coef + self.__tilt_coef_eps:
                return True
        return False

    @staticmethod    
    def show_lines(image: np.array, lines: list[list[tuple[int, int, int]]], show: bool = True) -> np.array:
        """
        Draw the extracted lines on given image.
        
        Parameters
        ----------
        image : np.array
            The image on which the extracted lines will be drawn
        lines : list[list[tuple[int, int, int, int]]]]
            Extracted lines that should be drawn. The lines is represented by a list in the following format: [(x1, y1, x2, y2)]
        
        Returns
        -------
        np.array
            The result image in which the extracted lines are drawn
        
        """

        image_with_lines = image.copy()
        # Iterate over points
        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points[0]

            # Drawing the lines
            cv2.line(
                image_with_lines,
                tuple(map(int, (x1, y1))),
                tuple(map(int, (x2, y2))),
                (0, 255, 0),
                2,
            )

        # Displaying an image with lines
        if show:
            cv2.imshow("lines", image_with_lines)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return image_with_lines


if __name__ == "__main__":
    che = ClockHandsExtractor(cv2.imread("./images/t1.png"), [400, 400], 399)
    che.extract()
    lines = che.get_extracted()
    print(lines)