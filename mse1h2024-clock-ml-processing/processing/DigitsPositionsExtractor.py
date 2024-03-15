# import requirements
import easyocr
import cv2


class DigitsPositionExtractor:
    """Class for extracting the positions of numbers from an image."""

    def __init__(self, image: any) -> None:
        """
        Initialization the DigitsPositionExtractor.

        Parameters
        ----------
        image : any
            Image object from which numbers are read
        """

        # Initializing an Image Object
        self.__image = image
        # Initialize an easyocr.Reader object with GPU permission
        self.__reader = easyocr.Reader(["en"], gpu=True)

    def get_boundaries(self) -> list[list[int]]:
        """
        This method returns the boundaries of recognized numbers in the image.
        The format is [x_min, x_max, y_min, y_max]
        """

        boundaries = self.__reader.detect(
            img=self.__image,
            optimal_num_chars=2,
            text_threshold=0.1,
            height_ths=0.1,
            width_ths=0.1,
            ycenter_ths=0.1,
            add_margin=0.23
        )[0][0]
        self.__show_boundaries(boundaries=boundaries)
        return boundaries

    def get_recognition(self) -> list[tuple[list[list[int]], str, int]]:
        """
        This method returns the recognized numbers and their corresponding bounds
        """

        recognition = self.__reader.readtext(
            image=self.__image,
            allowlist="0123456789",
            decoder='beamsearch',
            text_threshold=0.5,
            height_ths=0.1,
            width_ths=0.1,
            ycenter_ths=0.1,
            add_margin=0.23
        )
        self.__show_recognition(recognition=recognition)
        return recognition

    def get_image_without_digits(self, boundaries: list[list[int]]):
        """
            This method implements the removal of digits along recognized boundaries by painting areas containing
            digits with white color
        """

        image_without_digits = self.__image.copy()
        # Loop through recognized results
        for detection in boundaries:
            # Retrieving bounding box coordinates
            top_left = tuple(map(int, [detection[0], detection[2]]))
            bottom_right = tuple(map(int, [detection[1], detection[3]]))

            # Drawing the white box instead of digit
            image_without_digits = cv2.rectangle(image_without_digits, top_left, bottom_right, (255, 255, 255), -1)

        # Display an image without digits
        self.__display_image("Clear", image_without_digits)

        return image_without_digits

    def __show_boundaries(self, boundaries: list[list[int]]):
        """
            This method creates a new image based on the original one, draws the boundaries of the found digits on it,
            and displays the image on the screen
        """

        image_with_boxes = self.__image.clone()
        # Loop through recognized results
        for detection in boundaries:
            # Retrieving bounding box coordinates
            top_left = tuple(map(int, [detection[0], detection[2]]))
            bottom_right = tuple(map(int, [detection[1], detection[3]]))

            # Drawing the bounding box
            image_with_boxes = cv2.rectangle(image_with_boxes, top_left, bottom_right, (0, 255, 0), 2)

        # Display an image with bounding boxes
        self.__display_image("Boxes", image_with_boxes)

    def __show_recognition(self, recognition: list[tuple[list[list[int]], str, int]]):
        """
            This method creates a new image based on the original one, draws the boundaries of the found numbers
            and their recognition on it, and then displays the image on the screen
        """

        image_with_recognize_and_boxes = self.__image.clone()
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
        self.__display_image("Recognize", image_with_recognize_and_boxes)

    @staticmethod
    def __display_image(title: str, image: any):
        """
            This method displays the image on the screen
        """

        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    # File testing
    dpe = DigitsPositionExtractor(cv2.imread("t1.png"))
    result = dpe.get_recognition()
    print(*result, sep='\n')
