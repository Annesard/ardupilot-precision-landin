import cv2
import numpy as np
from pupil_apriltags import Detector  # pip install pupil-apriltags


# ==== Настройки камеры (примерные, потом заменишь на реальные) ====
# fx, fy, cx, cy — параметры калибровки камеры
FX = 600.0
FY = 600.0
CX = 320.0
CY = 240.0

CAMERA_MATRIX = np.array([[FX, 0, CX],
                          [0, FY, CY],
                          [0,  0,  1]], dtype=np.float32)

DIST_COEFFS = np.zeros((4, 1), dtype=np.float32)  # пока считаем, что дисторсии нет

# Реальный размер тега в метрах (замени на свой)
TAG_SIZE = 0.16  # 16 см


def create_detector():
    detector = Detector(
        families="tag36h11",
        nthreads=1,
        quad_decimate=1.0,
        quad_sigma=0.0,
        refine_edges=1,
        decode_sharpening=0.25,
        debug=0,
    )
    return detector


def detect_from_image(image_path: str):
    # Читаем изображение
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"[ERROR] Cannot read image: {image_path}")
        return

    detector = create_detector()

    # Вызываем детектор
    detections = detector.detect(
        img,
        estimate_tag_pose=True,
        camera_params=[FX, FY, CX, CY],
        tag_size=TAG_SIZE,
    )

    if len(detections) == 0:
        print("[INFO] No tags detected")
        return

    print(f"[INFO] Detected {len(detections)} tag(s)")

    for det in detections:
        # det.pose_t — это трёхмерный вектор (x, y, z) в камере
        tvec = det.pose_t.reshape(3)
        rvec = det.pose_R  # матрица 3x3

        print("Pose in camera frame (meters):")
        print(f"  x: {tvec[0]:.3f}, y: {tvec[1]:.3f}, z: {tvec[2]:.3f}")

        # Перевод в body-frame FRD (Forward-Right-Down) под ArduPilot
        # Допустим, что оси камеры:
        #   x_cam — вправо, y_cam — вниз, z_cam — вперёд
        # Тогда:
        #   forward (F) = z_cam
        #   right   (R) = x_cam
        #   down    (D) = y_cam
        forward = tvec[2]
        right = tvec[0]
        down = tvec[1]

        print("Pose in body-frame FRD (for LANDINGTARGET):")
        print(f"  forward: {forward:.3f} m")
        print(f"  right:   {right:.3f} m")
        print(f"  down:    {down:.3f} m")
        print("-----")


if __name__ == "__main__":
    detect_from_image("tag36h11-0.png")

