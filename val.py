from ultralytics import YOLO
import torch

model = YOLO("c:/Users/chase/runs/detect/train6/weights/best.pt")
# Evaluate model performance on the validation set
metrics = model.val()
print(metrics.box.map)  # map50-95
print(metrics.box.map50)  # map50
print(metrics.box.map75)  # map75
print(metrics.box.maps)  # a list contains map50-95 of each category

# Perform object detection on an image
results = model('c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/dataset/images/val/00616.jpg')
results[0].show()