from ultralytics import YOLO

model = YOLO("weights/best.pt")

results = model.predict(
    source="test.jpg",
    conf=0.25,
    save=True
)