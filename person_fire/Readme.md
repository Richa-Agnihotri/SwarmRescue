# SwarmRescue Person + Fire Detector

Model: YOLO11n

Classes:
0 - person
1 - fire

Training:
- Epochs: 50
- Image Size: 640

Performance:
- Precision: 0.508
- Recall: 0.428
- mAP50: 0.425
- mAP50-95: 0.166

Usage:

from ultralytics import YOLO

model = YOLO("best.pt")
results = model("image.jpg")