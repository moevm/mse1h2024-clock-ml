# import requirements
import easyocr
import cv2
import numpy as np


class ClockDigitsExtractor:
    """Class for extracting the positions of clock numbers from an image."""

    def __init__(self) -> None:
        """Initialization the DigitsPositionExtractor."""

        self.__digits = list()
        self.__boundaries = list()

        # Initialize an easyocr.Reader object with GPU permission
        self.__reader = easyocr.Reader(["en"], gpu=True)

    def extract_boundaries(self, image: np.array) -> list[list[int, int, int, int]] | None:
        """
        This method returns the boundaries of recognized numbers in the image.
        The boundaries is represented by a list in the following format: [[x_min, x_max, y_min, y_max]]
        
        Parameters
        ----------
        image : np.array
            Image object from which numbers are read
        """
        
        self.__boundaries = self.__reader.detect(
            # img=image,
            # optimal_num_chars=2,
            # text_threshold=0.1,
            # height_ths=0.1,
            # width_ths=0.1,
            # ycenter_ths=0.1,
            # add_margin=0.23
            img=image,
            text_threshold=0.5,
            link_threshold=0.8,
            ycenter_ths=0.2,
            height_ths=0.1,
            width_ths=0.1,
            add_margin=0.23,
        )[0][0]

        return self.__boundaries if self.__boundaries else None
        
    def extract(self, image: np.array) -> list[tuple[list[list[int, int], list[int, int], list[int, int], list[int, int]], str, int]] | None:
        """
        This method returns the recognized numbers and their corresponding bounds.
        The boundaries is represented by a list in the following format: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]

        Parameters
        ----------
        image : np.array
            Image object from which numbers are read
        """
        
        self.__digits = self.__reader.readtext(
            image=image,
            allowlist="0123456789",
            decoder='beamsearch',
            text_threshold=0.5,
            link_threshold=0.8,
            ycenter_ths=0.2,
            height_ths=0.1,
            width_ths=0.1,
            add_margin=0.23,
        )

        return self.__digits if self.__digits else None
        
    @staticmethod
    def show_without_digits(image: np.array, boundaries: list[list[int, int, int, int]], show: bool = True) -> np.array:
        """
            This method implements the removal of digits along recognized boundaries by painting areas containing
            digits with white color.
            The boundaries is represented by a list in the following format: [[x_min, x_max, y_min, y_max]]
        """

        image_without_digits = image.copy()
        # Loop through recognized results
        for detection in boundaries:
            # Retrieving bounding box coordinates
            top_left = tuple(map(int, [detection[0], detection[2]]))
            bottom_right = tuple(map(int, [detection[1], detection[3]]))

            # Drawing the white box instead of digit
            image_without_digits = cv2.rectangle(image_without_digits, top_left, bottom_right, (255, 255, 255), -1)

        # Display an image without digits
        if show:
            ClockDigitsExtractor.display_image("Clear", image_without_digits)

        return image_without_digits

    @staticmethod
    def show_boundaries(image: np.array, boundaries: list[list[int, int, int, int]], show: bool = True) -> np.array:
        """
            This method creates a new image based on the original one, draws the boundaries of the found digits on it,
            and displays the image on the screen.
            The boundaries is represented by a list in the following format: [[x_min, x_max, y_min, y_max]]
        """

        image_with_boxes = image.copy()
        # Loop through recognized results
        for detection in boundaries:
            # Retrieving bounding box coordinates
            top_left = tuple(map(int, [detection[0], detection[2]]))
            bottom_right = tuple(map(int, [detection[1], detection[3]]))

            # Drawing the bounding box
            image_with_boxes = cv2.rectangle(image_with_boxes, top_left, bottom_right, (0, 255, 0), 2)

        # Display an image with bounding boxes
        if show:
            ClockDigitsExtractor.display_image("Boxes", image_with_boxes)
        
        return image_with_boxes

    @staticmethod
    def show_recognition(image: np.array, recognition: list[tuple[list[list[int, int], list[int, int], list[int, int], list[int, int]], str, int]], show: bool = True) -> np.array:
        """
            This method creates a new image based on the original one, draws the boundaries of the found numbers
            and their recognition on it, and then displays the image on the screen.
            The boundaries is represented by a list in the following format: [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
        """

        image_with_recognize_and_boxes = image.copy()
        # Loop through recognized results
        for detection in recognition:
            # Extract bounding box coordinates and recognized text
            top_left = tuple(map(int, detection[0][0]))
            bottom_right = tuple(map(int, detection[0][2]))
            text = detection[1]

            # Drawing bounding box and text on the image
            image_with_recognize_and_boxes = cv2.rectangle(
                image_with_recognize_and_boxes, top_left, bottom_right, (0, 255, 0), 2)
            image_with_recognize_and_boxes = cv2.putText(
                image_with_recognize_and_boxes, text, top_left, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )

        # Displaying an image with bounding boxes and recognized numbers
        if show:
            ClockDigitsExtractor.display_image("Recognize", image_with_recognize_and_boxes)
        
        return image_with_recognize_and_boxes

    @staticmethod
    def display_image(title: str, image: np.array) -> None:
        """This method displays the image on the screen"""

        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    cde = ClockDigitsExtractor()
    result = cde.extract(cv2.imread("./images/t1.png"))
    #cde.show_recognition(cv2.imread("./images/t1.png"), result)
    print(*result, sep='\n')
    