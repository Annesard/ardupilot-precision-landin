# AprilTag-based Precision Landing

Проект по визуальной локализации посадочной площадки с помощью AprilTag.
Базовый метод (baseline) оценивает позу маркера в координатах камеры и преобразует её в body-frame FRD (Forward-Right-Down), совместимый с MAVLink `LANDING_TARGET`.

## Project Structure

```
ardupilot-precision-landin/
├── src/
│   ├── notebooks/
│   │   └── prototype.ipynb     # Baseline: AprilTag pose estimation
│   ├── prototype.py            # Standalone Python script
│   ├── tag36h11-0.png          # Test AprilTag image (tag36h11 family)
│   └── tag36h11-0.svg
├── requirements.txt
└── README.md
```

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Baseline Method

The baseline pipeline consists of three steps:

1. **AprilTag Detection** — detect `tag36h11` family marker in a grayscale image using `pupil_apriltags`
2. **Pose Estimation** — estimate 6-DoF pose (tvec) in camera frame using known camera intrinsics and physical tag size
3. **FRD Conversion** — transform camera-frame coordinates into body-frame FRD for MAVLink `LANDING_TARGET`:
   - `forward = tvec[2]` (camera Z → drone forward)
   - `right   = tvec[0]` (camera X → drone right)
   - `down    = tvec[1]` (camera Y → drone down)

### Camera Parameters (Baseline)

| Parameter | Value |
|-----------|-------|
| FX (focal length X) | 600.0 px |
| FY (focal length Y) | 600.0 px |
| CX (principal point X) | 320.0 px |
| CY (principal point Y) | 240.0 px |
| Distortion coefficients | zeros (no distortion assumed) |
| Tag size | 0.16 m (16 cm) |
| Tag family | tag36h11 |

## Baseline Results

Test input: `src/tag36h11-0.png`

![AprilTag test image](src/tag36h11-0.png)

### Detection Output

```
[INFO] Detected 1 tag(s)
Pose in camera frame (meters):
  x: -0.100, y: -0.050, z: 0.375
Pose in body-frame FRD (for LANDING_TARGET):
  forward:  0.375 m
  right:   -0.100 m
  down:    -0.050 m
```

### Metrics Table

| Axis | Camera Frame | Body-Frame FRD | Meaning |
|------|-------------|----------------|---------|
| X / Right  | -0.100 m | right:   -0.100 m | Tag is 10 cm to the left |
| Y / Down   | -0.050 m | down:    -0.050 m | Tag is 5 cm above camera |
| Z / Forward|  0.375 m | forward:  0.375 m | Tag is 37.5 cm away |

**Interpretation:** The AprilTag was successfully detected at ~37.5 cm in front of the camera, 10 cm to the left, and 5 cm above the camera center. The output is directly compatible with MAVLink `LANDING_TARGET` message format.

## Usage

Run the Jupyter notebook:
```bash
cd src/notebooks
jupyter notebook prototype.ipynb
```

Or run the standalone script:
```bash
cd src
python prototype.py
```

## Dependencies

See [`requirements.txt`](requirements.txt):

| Package | Purpose |
|---------|----------|
| `numpy` | Array and matrix operations |
| `opencv-python` | Image loading and processing |
| `pupil-apriltags` | AprilTag detection and pose estimation |
| `jupyter` | Notebook interface |
