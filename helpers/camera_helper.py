import cv2


def initialize_camera(index=0):
    """Initialize the camera and return the video capture object.

    Args:
        index (int): The index of the camera to open. Default is 0 (primary camera).

    Returns:
        cv2.VideoCapture: The video capture object for the camera.

    Raises:
        ValueError: If the camera cannot be opened.
    """
    video_source = cv2.VideoCapture(index)
    if not video_source.isOpened():
        raise ValueError(f"Unable to open the camera with index {index}")
    return video_source
