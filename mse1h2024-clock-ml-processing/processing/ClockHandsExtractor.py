# import requirements
import cv2
import numpy as np


class ClockHandsExtractor:
    """Class for extracting the positions of clock hands from an image."""

    def __init__(self, image: np.array, center: list[int] = [444, 437], radius: int = 280) -> None:
        self.__image = image
        self.__gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        self.__clock_hands = list()
        self.__center = center
        self.__center_eps = radius/4
        self.__min_arrow_length = radius/5
        self.__tilt_angle_eps = 0.05

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

    def __select_arrows(self, lines: list) -> None:
        
        self.__show_clock_hands(lines)
        tilt_angles = set()
        for line in lines:
            (x1, y1, x2, y2) = line[0]
            tilt_angle = (y2-y1)/(x2-x1)
            if (
                (
                    self.__center[0] - self.__center_eps <= x1 <= self.__center[0] + self.__center_eps
                    and self.__center[1] - self.__center_eps <= y1 <= self.__center[1] + self.__center_eps
                )
                or (
                    self.__center[0] - self.__center_eps <= x2 <= self.__center[0] +  self.__center_eps
                    and self.__center[1] - self.__center_eps <= y2 <= self.__center[1] +  self.__center_eps
                )
            ) and np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) >= self.__min_arrow_length and not self.__is_exist_tilt_angle(tilt_angle, tilt_angles):
                # print(line)
                # add new line
                self.__clock_hands.append((x1, y1, x2, y2))
                self.__show_clock_hands([line])
                
                # update existing tilt angles
                tilt_angles.add(tilt_angle)
                print(tilt_angle)

            
        #for i in range(len(self.__clock_hands)):

    def __is_exist_tilt_angle(self, tilt_angle: float, tilt_angles: set[float]) -> bool:
        for cur_tilt_angle in tilt_angles:
            if cur_tilt_angle - self.__tilt_angle_eps <= tilt_angle <= cur_tilt_angle + self.__tilt_angle_eps:
                return True
        return False

        
    def __show_clock_hands(self, lines: list) -> None:
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
    che = ClockHandsExtractor(cv2.imread("./images/t1.png"), [450, 421], 399)
    che.extract()
    lines = che.get_clock_hands_position()
    print(lines, len(lines))
