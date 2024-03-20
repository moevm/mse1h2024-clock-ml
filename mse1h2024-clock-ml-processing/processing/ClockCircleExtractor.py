# import requirements
import cv2
import numpy as np


class ClockCircleExtractor:
    """Class for extracting the positions and radius for clock circle from the input image"""

    def __init__(self, image: np.array) -> None:
        """
        Initialization the ClockCircleExtractor.

        Parameters
        ----------
        image : np.array
            Input image with clock
        
        """
        
        self.__src_image = image
        self.__gray_image = cv2.cvtColor(self.__src_image, cv2.COLOR_BGR2GRAY)
        
        self.__clock_circle = None

    def get_extracted(self) -> list[int, int, int] | None:
        """Return the exctracted clock circle from image or None if not found"""
        
        return self.__clock_circle

    def extract(self) -> None:
        """
        Extract clock circle from the input image and save it in class instance. 
        To get extracted circle use `get_extracted()` method.
        
        """
        
        finded_circles = cv2.HoughCircles(
            image=self.__gray_image,
            method=cv2.HOUGH_GRADIENT_ALT,
            dp=1,
            minDist=10,
            param2=0,
            minRadius=0,
            maxRadius=self.__src_image.shape[0],
        )
        
        if finded_circles is None:
            print('Not found circle on input image')
            return
        exctracted = finded_circles[0]
        
        # define clock circle as circle with maximum radius
        exctracted = np.int32(exctracted)
        largest_circle = max(exctracted, key=lambda elem: elem[2])
        self.__clock_circle = largest_circle

    @staticmethod
    def show_circles(image: np.array, finded_circles: list[list[int, int, int]], show: bool = True) -> np.array:
        """
        Draw the extracted circles on given image.
        
        Parameters
        ----------
        image : np.array
            The image on which the extracted circles will be drawn
        finded_circles : list[list[int, int, int]]
            Extracted circles that should be drawn. The circle is represented by a list in the following format: [centerX, centerY, radius]
        show : bool
            If True, displays the resulting image. Default value is True.

        Returns
        -------
        np.array
            The result image in which the extracted circles are drawn
        
        """
        result_image = image.copy()
        for circle in finded_circles:
            center, radius = (circle[0], circle[1]), circle[2]
            cv2.circle(
                result_image,
                center=center,
                radius=radius,
                color=(0, 255, 0),
                thickness=2,
            ) 
            # draw center
            cv2.circle(
                result_image,
                center,
                radius=10,
                color=(0, 0, 255),
                thickness=cv2.FILLED,
            )

        if show:
            cv2.imshow("circle", result_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
        return result_image


if __name__ == "__main__":
    image = cv2.imread("./images/t1.png")
    circle_extractor = ClockCircleExtractor(
        image=image,
    )

    circle_extractor.extract()
    clock_circle = circle_extractor.get_extracted()
    # ClockCircleExtractor.show_circles(image, [clock_circle])
