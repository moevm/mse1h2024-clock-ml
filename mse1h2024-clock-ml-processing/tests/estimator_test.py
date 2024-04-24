import pytest
import cv2
from processing.Estimator import Estimator


class TestEstimator:

    estimator = Estimator()

    @pytest.mark.parametrize("estimation_result", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_estimation(self, estimation_result):
        image_filename = f"tests/images/{estimation_result}.png"
        image = cv2.imread(filename=image_filename)

        try:
            result = self.estimator.estimate(image=image, time=(11, 5))
        except Exception as e:
            print(f"Some problem in estimator: {e}")

        assert result == estimation_result
