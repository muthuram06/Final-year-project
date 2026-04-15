import cv2
from feature_extraction.video_features import run_head_pose


def test_camera():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not working")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Webcam Test", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Uncomment this if you only want to test camera
    # test_camera()

    run_head_pose()