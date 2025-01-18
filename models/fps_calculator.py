import time


class FPSCalculator:
    """
    Class to calculate the frames per second (FPS) of a video stream

    Attributes:
        _start_time: float - the time when the FPS calculation started
        _frame_count: int - the number of frames processed
        _fps: float - the calculated FPS value

    Methods:
        update: increment the frame count and update the FPS value
        get_fps: get the calculated FPS value
    """

    def __init__(self):
        """
        Initialize the FPSCalculator object
        """
        self._start_time = time.time()
        self._frame_count = 0
        self._fps = 0

    def update(self):
        """
        increment the frame count and update the FPS value based on the elapsed time
        """
        self._frame_count += 1
        current_time = time.time()
        elapsed_time = current_time - self._start_time

        if elapsed_time >= 1:
            self._fps = self._frame_count / elapsed_time
            self._frame_count = 0
            self._start_time = current_time

    def get_fps(self):
        """
        get the calculated FPS value
        """
        return self._fps
