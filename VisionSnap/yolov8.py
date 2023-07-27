from ultralytics import YOLO

# Load a model
model = YOLO("yolov8x.yaml")  # build a new model from scratch
model = YOLO("yolov8x.pt")  # load a pretrained model (recommended for training)

# Use the model
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image

print(results)