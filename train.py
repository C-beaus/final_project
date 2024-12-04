from ultralytics import YOLO
from ultralytics.data.converter import convert_coco
import torch

# convert_coco(labels_dir='c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/Town01_Opt_120_color/Town01_Opt_120/ClearNoon/bboxes')

# Load a model
model = YOLO("yolo11n.pt")
# model = YOLO("yolo11s.pt") # to try, should give better accuracy but slower

# Train the model
train_results = model.train(
    data="dataset/data_desc.yaml",  # path to dataset YAML #data_desc
    epochs=100,  # number of training epochs
    imgsz=640,  # training image size
    device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
)

# Val
# Evaluate model performance on the validation set
metrics = model.val()
print(metrics.box.map)  # map50-95
print(metrics.box.map50)  # map50
print(metrics.box.map75)  # map75
print(metrics.box.maps)  # a list contains map50-95 of each category

# Perform object detection on an image
results = model('c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/dataset/images/val/00000.jpg')
results[0].show()

# Export the model to ONNX format
path = model.export(format="onnx")  # return path to exported model