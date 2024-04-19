import cv2


class TestCircleExtractor:
    from processing.extractors.ClockCircleExtractor import ClockCircleExtractor

    extractor = ClockCircleExtractor()

    def test_extract_not_none(self):
        try:
            image = cv2.imread("tests/images/10.png")
            result = self.extractor.extract(image=image)
        except Exception as e:
            print(f"Some problem in test clock extractor: {e}")

        assert result is not None

    def test_extract_none(self):
        try:
            image = cv2.imread("tests/images/1.png")
            result = self.extractor.extract(image=image)
        except Exception as e:
            print(f"Some problem in test clock extractor: {e}")

        assert result is None


class TestDigitsExtractor:
    from processing.extractors.ClockDigitsExtractor import ClockDigitsExtractor

    extractor = ClockDigitsExtractor()

    def test_extract_not_none(self):
        try:
            image = cv2.imread("tests/images/10.png")
            result = self.extractor.extract(image=image)
        except Exception as e:
            print(f"Some problem in test digits extractor: {e}")

        assert result is not None

    def test_extract_none(self):
        try:
            image = cv2.imread("tests/images/1.png")
            result = self.extractor.extract(image=image)
        except Exception as e:
            print(f"Some problem in test digits extractor: {e}")

        assert result is None


class TestClockHandsExtractor:
    from processing.extractors.ClockHandsExtractor import ClockHandsExtractor

    extractor = ClockHandsExtractor()

    def test_extract_not_none(self):
        try:
            image = cv2.imread("tests/images/10.png")
            result = self.extractor.extract(image=image, center=[469, 221], radius=192)
        except Exception as e:
            print(f"Some problem in test digits extractor: {e}")

        assert result is not None

    def test_extract_none(self):
        try:
            image = cv2.imread("tests/images/1.png")
            result = self.extractor.extract(image=image, center=[0, 0], radius=1)
        except Exception as e:
            print(f"Some problem in test digits extractor: {e}")

        assert result is None
