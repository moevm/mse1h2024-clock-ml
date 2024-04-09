import numpy as np

REFERENCE_DIGITS_ANGLES = {i: np.mod(i * 30, 360) for i in range(1, 13)}
