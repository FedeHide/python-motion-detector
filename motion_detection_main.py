import cv2
from datetime import datetime
from models.fps_calculator import FPSCounter
from helpers.frames_processor import process_frame
from helpers.camera_helper import initialize_camera
from helpers.motion_state import handle_state_change
from helpers.motion_intervals import compute_motion_intervals


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
    timestamp_list = []
    video_source = None
    initial_frame = None

    try:
        video_source = initialize_camera()
        frame_rate_monitor = FPSCounter(smoothing_interval=2)

        while True:
            is_frame_read, captured_frame = video_source.read()
            if not is_frame_read:
                print("Failed to read frame")
                break

            video_frame, processed_frame, detection_status = process_frame(
                captured_frame, initial_frame
            )

            if initial_frame is None:
                initial_frame = processed_frame
                continue

            status_list, timestamp_list = handle_state_change(
                status_list, timestamp_list, detection_status
            )

            frame_rate_monitor.update_frame_rate()
            current_fps = frame_rate_monitor.get_fps()
            # Display the frame rate on the video feed
            cv2.putText(
                video_frame,
                f"FPS: {current_fps:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            # Display the processed frame
            cv2.imshow("Motion Detection", video_frame)

            # Check for the 'q' key to exit the loop
            exit_key = cv2.waitKey(10) & 0xFF
            if exit_key == ord("q"):
                if detection_status == 1:
                    timestamp_list.append(datetime.now())
                break

    except cv2.error as e:
        print(f"OpenCV error: {e}")

    except ValueError as e:
        print(f"Value error: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        motion_intervals_df = compute_motion_intervals(timestamp_list)
        motion_intervals_df.to_csv("motion_intervals.csv", index=False)
        if video_source is not None:
            video_source.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run_motion_detection()
