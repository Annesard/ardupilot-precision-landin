# AprilTag-based Precision Landing

Проект по визуальной локализации посадочной площадки с помощью AprilTag. Базовый метод (baseline) оценивает позу маркера в координатах камеры и преобразует её в body-frame FRD (Forward-Right-Down), совместимый с MAVLink LANDING_TARGET.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
