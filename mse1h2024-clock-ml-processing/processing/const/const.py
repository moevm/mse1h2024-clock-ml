DELTA_DIGIT_ANGLE = 15
REFERENCE_DIGITS_ANGLES = {i: i * 30 for i in range(1, 13)}

ABSOLUTE_MOD = lambda angle: min(360 - angle, angle)
CHECK_ANGLE = (
    lambda angle, delta, value_to_check: ABSOLUTE_MOD(
        (angle - value_to_check + 360) % 360
    )
    <= delta
)
