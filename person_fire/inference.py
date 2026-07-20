from ultralytics import YOLO

model = YOLO("best.pt")

results = model.predict(
    source="test.jpg",
    conf=0.25,
    save=True
)