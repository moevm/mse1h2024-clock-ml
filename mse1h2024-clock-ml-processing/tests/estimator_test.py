import pytest
import cv2
from processing.Estimator import Estimator


class TestEstimator:

    estimator = Estimator()

    @pytest.mark.parametrize("estimation_result", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_estimation(self, estimation_result):
        image_filename = f"tests/images/{estimation_result}.png"
        image = cv2.imread(filename=image_filename)

        result = self.estimator.estimate(image=image, time=0)
        assert result == estimation_result
