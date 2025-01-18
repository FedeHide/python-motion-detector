import cv2


def process_frame(frame, first_frame=None, min_contour_area=1000):
    """
    Process a video frame for motion detection.

    Args:
        frame (numpy.ndarray): The current frame from the video feed.
        first_frame (numpy.ndarray, optional): The initial frame for comparison. Defaults to None.
        min_contour_area (int, optional): Minimum area for contours to be considered motion. Defaults to 1000.

    Returns:
        tuple: Processed frame, updated first frame, motion status (1 if motion detected, 0 otherwise).
    """
    status = 0

    # convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # initialize the first frame if not provided
    if first_frame is None:
        first_frame = gray
        return frame, gray, status

    # compute the absolute difference between the current frame and the first frame
    delta_frame = cv2.absdiff(first_frame, gray)
    # apply threshold to get binary image
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # dilate the threshold frame to fill in holes
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # find contours in the threshold frame
    contours, _ = cv2.findContours(
        thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # process contours to detect motion
    for contour in contours:
        if cv2.contourArea(contour) < min_contour_area:
            continue
        status = 1  # motion detected

        # draw bounding box around the motion
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    return frame, first_frame, status
