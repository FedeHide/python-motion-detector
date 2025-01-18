import cv2, time
from models.fps_calculator import FPSCalculator


def motion_detector():
    """ """
    try:
        video = cv2.VideoCapture(0)

        # check if the camera is opened
        if not video.isOpened():
            raise ValueError("Unable to open the camera")

        fps_calculator = FPSCalculator(smoothing_interval=2)

        while True:
            check, frame = video.read()

            if not check:
                print("Failed to read frame")
                break

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
