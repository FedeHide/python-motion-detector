import cv2
from models.fps_calculator import FPSCounter
from helpers.frames_processor import process_frame
from helpers.camera_helper import initialize_camera
from helpers.motion_state import handle_state_change


def run_motion_detection():
    """This script captures video frames from a camera and performs motion detection in real-time.

    It utilizes OpenCV for frame capture and display, and custom modules to handle motion state changes,
    process frames, and calculate FPS.

    Key functions:
    - Initializes the camera and captures video frames.
    - Processes each frame for motion detection.
    - Calculates and displays the frames per second (FPS).
    - Handles state changes (motion detected or not) and logs relevant data.
    - Exits gracefully upon pressing the 'q' key or encountering an error.

    Modules:
    - `FPSCounter`: Calculates frames per second with smoothing.
    - `process_frame`: Processes each frame to detect motion and handle state changes.
    - `initialize_camera`: Initializes the camera for video capture.
    - `handle_state_change`: Handles motion state changes and stores timestamps.

    Exceptions:
    - Handles OpenCV errors, value errors, and any unexpected errors.

    Finally, releases the camera and closes all OpenCV windows when the program ends.
    """

    status_list = [None, None]
    times = []
    video = None
    try:
        video = initialize_camera()
        first_frame = None

        fps_calculator = FPSCounter(smoothing_interval=2)

        while True:
            check, frame = video.read()
            if not check:
                print("Failed to read frame")
                break

            frame, first_frame, status = process_frame(frame, first_frame)

            status_list, times = handle_state_change(status_list, times, status)

            fps_calculator.update()
            fps = fps_calculator.get_fps()
            cv2.putText(
                frame,
                f"FPS: {fps:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.imshow("Motion Detection", frame)
            key = cv2.waitKey(10) & 0xFF
            if key == ord("q"):
                break

    except cv2.error as e:
        print(f"OpenCV error: {e}")

    except ValueError as e:
        print(f"Value error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        if video is not None:
            video.release()
        cv2.destroyAllWindows()
