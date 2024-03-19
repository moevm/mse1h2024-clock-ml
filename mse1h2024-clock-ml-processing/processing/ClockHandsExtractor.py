# import requirements
import cv2
import numpy as np


class ClockHandsExtractor:
    """Class for extracting the positions of clock hands from an image."""

    def __init__(self, image: any, center: list[int] = [444, 437]) -> None:
        self.__image = image
        self.__gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.__clock_hands = list()
        self.__center = center

    def get_clock_hands_position(self) -> list:
        return self.__clock_hands

    def extract(self) -> None:
        line_segment_detector = cv2.createLineSegmentDetector(
            refine=cv2.LSD_REFINE_STD,
            # sigma_scale=2, #длиннее палки
            # quant=2.0,
            # ang_th = 80, #ideal
            density_th=0.1,  # ideal
        )

        lines = line_segment_detector.detect(
            image=self.__gray_image,
        )[0]

        self.__select_arrows(lines)

        # mask = self.__show_clock_hands(lines)

    def __select_arrows(self, lines) -> None:
        eps = 20
        self.__show_clock_hands(lines)
        for line in lines:
            (x1, y1, x2, y2) = line[0]
            if (
                (
                    self.__center[0] - eps <= x1 <= self.__center[0] + eps
                    and self.__center[1] - eps <= y1 <= self.__center[1] + eps
                )
                or (
                    self.__center[0] - eps <= x2 <= self.__center[0] + eps
                    and self.__center[1] - eps <= y2 <= self.__center[1] + eps
                )
            ) and np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) > 30:
                print(line)
                self.__clock_hands.append((x1, y1, x2, y2))
                self.__show_clock_hands([line])

    def __show_clock_hands(self, lines) -> None:
        image_with_clock_hands = self.__image.copy()
        # mask = np.zeros_like(self.__gray_image)
        # Iterate over points
        for points in lines:
            # Extracted points nested in the list
            x1, y1, x2, y2 = points[0]
            # Draw the lines join the points
            # On the original image
            cv2.line(
                image_with_clock_hands,
                tuple(map(int, (x1, y1))),
                tuple(map(int, (x2, y2))),
                (0, 255, 0),
                2,
            )

            # cv2.line(
            #     mask,
            #     tuple(map(int, (x1, y1))),
            #     tuple(map(int, (x2, y2))),
            #     255,
            #     2,
            # )

        # Displaying and save an image with clock hands
        cv2.imshow("clock-hands", image_with_clock_hands)
        cv2.imwrite("result/clock_hands.png", image_with_clock_hands)

        # cv2.imshow("mask", mask)
        # cv2.imwrite("result/mask.png", mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # return mask


if __name__ == "__main__":
    che = ClockHandsExtractor(cv2.imread("./images/t1_clear.png"))
    che.extract()
    lines = che.get_clock_hands_position()
    print(lines, len(lines))
