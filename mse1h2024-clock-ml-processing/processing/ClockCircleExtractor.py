# import requirements
import cv2
import numpy as np


class ClockCircleExtractor:
    """_summary_"""

    def __init__(self, image: np.array) -> None:
        self.__src_image = image
        self.__gray_image = cv2.cvtColor(self.__src_image, cv2.COLOR_BGR2GRAY)
        
        self.__clock_circle = None

    def get_clock_circle_position(self) -> list[int, int, int]:
        return self.__clock_circle

    def extract(self) -> None:
        finded_circles = cv2.HoughCircles(
            image=self.__gray_image,
            method=cv2.HOUGH_GRADIENT_ALT,
            dp=1,
            minDist=10,
            param2=0,
            minRadius=0,
            maxRadius=self.__src_image.shape[0],
        )[0]

        # define clock circle as circle with maximum radius
        finded_circles = np.int32(finded_circles)
        largest_circle = max(finded_circles, key=lambda elem: elem[2])
        self.__clock_circle = largest_circle

        self.__show_clock_circle([largest_circle])

    def __show_clock_circle(self, finded_circles: list) -> None:
        for circle in finded_circles:
            center, radius = (circle[0], circle[1]), circle[2]
            cv2.circle(
                self.__src_image,
                center=center,
                radius=radius,
                color=(0, 255, 0),
                thickness=2,
            )
            # draw center
            cv2.circle(
                self.__src_image,
                center,
                radius=10,
                color=(0, 0, 255),
                thickness=cv2.FILLED,
            )

        cv2.imshow("circle", self.__src_image)
        cv2.imwrite("result/circle.png", self.__src_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    image = cv2.imread("./images/t1.png")
    extractor = ClockCircleExtractor(
        image=image,
    )

    extractor.extract()
    print(extractor.get_clock_circle_position())
