# import requirements
import cv2
import numpy as np
from processing.objects.objects import ClockHands


class ClockHandsExtractor:
    """Class for extracting the positions of clock hands from an image."""

    def __init__(self, angle_eps: float = 5) -> None:
        """Initialization the ClockHandsExtractor."""

        # Initializing a clock hands list
        self.__clock_hands = None

        # Initializing a basic constants
        self.__angle_eps = angle_eps
        self.__center = None
        self.__center_eps = None
        self.__min_clock_hand_length = None

    def __clear_previous(self):
        """This method clears internal variables from previous recognition"""

        self.__clock_hands = None

    def __set_constants(self, center: list[int, int], radius: int) -> None:
        """This method sets basic constants"""

        self.__center = center
        self.__center_eps = radius / 3
        self.__min_clock_hand_length = radius / 5

    def extract(
        self, image: np.array, center: list[int, int], radius: int
    ) -> ClockHands | None:
        """
        This method extracts clock hands from an image.

        Parameters
        ----------
        image : np.array
            Image object from which numbers are read
        center : list[int, int]
            Сenter point of the dial or image [x, y]
        radius : int
            Radius of the dial or the maximum circle inscribed in the image
        """
        self.__clear_previous()
        # set given parameters for extracting
        self.__set_constants(center, radius)

        # Initializing an Image Object
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Initializing the line detector
        line_segment_detector = cv2.createLineSegmentDetector(
            refine=cv2.LSD_REFINE_STD,
            # sigma_scale=2, # длиннее палки
            # quant=2.0,
            # ang_th = 80, # ideal
            density_th=0.1,  # Minimal density of aligned region points in the enclosing rectangle.
        )

        # Detection of all lines
        lines = line_segment_detector.detect(
            image=gray_image,
        )[0]

        if lines is None:
            print("Not found lines on input image")
            return

        # Selecting lines that are clock hands
        self.__select_clock_hands(lines)

        return self.__clock_hands

    def __select_clock_hands(
        self, lines: list[list[tuple[int, int, int, int]]]
    ) -> None:
        """ "
        This method selects the lines that are the hands of the clock

        Parameters
        ----------
        lines : list[list[tuple[int, int, int, int]]]
            list of lines, among which you need to select the ones responsible for the clock lines.
            The lines is represented by a list in the following format: [(x1, y1, x2, y2)].
        """

        # Initializing set tilt coefficients for recognized clock hands
        angles = set()

        hands_coordinates = []
        for line in lines:
            (x1, y1, x2, y2) = line[0]

            angle_degrees = self.__define_angle(x1, y1, x2, y2)

            if (
                self.__shortest_distance(self.__center, (x1, y1), (x2, y2))[0]
                <= self.__center_eps
                and np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                >= self.__min_clock_hand_length
                and not self.__is_exist_angle(angle_degrees, angles)
            ):
                # Add new line to clock hands
                hands_coordinates.append((x1, y1, x2, y2))
                point = self.__shortest_distance(self.__center, (x1, y1), (x2, y2))[1]
                # self.show_lines(self.__image, [line, [(*self.__center, *point)]])
                # self.show_lines(self.__image, [[(*self.__center, *point)]])

                # Update existing tilt coefficients
                angles.add(angle_degrees)

        if len(hands_coordinates) == 2:
            self.__clock_hands = ClockHands(hands_coordinates)

    def __define_angle(self, x1, y1, x2, y2) -> float:
        """This method is used to determine the angle of the hand relative to the center of the watch"""
        
        x_start, x_end = (
            (x1, x2)
            if abs(self.__center[0] - x1) < abs(self.__center[0] - x2)
            else (x2, x1)
        )
        y_start, y_end = (
            (y1, y2)
            if abs(self.__center[1] - y1) < abs(self.__center[1] - y2)
            else (y2, y1)
        )
        dx = x_end - x_start
        dy = y_end - y_start

        angle = np.arctan2(dx, -dy)
        angle_degrees = np.round(np.degrees(angle), 3)
        if angle_degrees < 0:
            angle_degrees += 360.0

        return angle_degrees

    def __shortest_distance(
        self,
        point: list[int, int],
        line_start: list[int, int],
        line_end: list[int, int],
    ) -> tuple[float, np.ndarray[float, float]]:
        """This method calculates the shortest distance from a point to a line given by the start and end coordinates"""

        point = np.array(point)
        line_start = np.array(line_start)
        line_end = np.array(line_end)

        line_vector = line_end - line_start
        point_vector = point - line_start

        line_length_squared = np.dot(line_vector, line_vector)
        t = np.dot(point_vector, line_vector) / line_length_squared

        if t < 0:
            closest_point = line_start
        elif t > 1:
            closest_point = line_end
        else:
            closest_point = line_start + t * line_vector

        return (np.linalg.norm(point - closest_point), closest_point)

    def __is_exist_angle(self, angle: float, angles: set[float]) -> bool:
        """This method checks for the presence of a clock hand with the same slope factor"""

        for cur_angle in angles:
            if cur_angle - self.__angle_eps <= angle <= cur_angle + self.__angle_eps:
                return True
        return False

    @staticmethod
    def show_lines(
        image: np.array,
        lines: list[list[tuple[int, int, int, int]]] | ClockHands,
        show: bool = True,
    ) -> np.array:
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
        if isinstance(lines, ClockHands):
            lines = lines.clock_hands
        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points

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
    che = ClockHandsExtractor()
    lines = che.extract(cv2.imread("./images/t1.png"), [400, 400], 399)
    print(lines)
