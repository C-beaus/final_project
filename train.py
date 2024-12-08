from ultralytics import YOLO
from ultralytics.data.converter import convert_coco
import torch

# convert_coco(labels_dir='c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/Town01_Opt_120_color/Town01_Opt_120/ClearNoon/bboxes')


if __name__ == '__main__':
    # Load a model
    model = YOLO("yolo11n.pt")
    # model = YOLO("ultralytics_output/second_attempt3/weights/last.pt")
    # model = YOLO("yolo11s.pt") # to try, should give better accuracy but slower
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Cuda? {torch.cuda.is_available()} and {dev}")

    # Train the model
    train_results = model.train(
        data="dataset/data_desc.yaml",  # path to dataset YAML #data_desc
        epochs=200,  # number of training epochs
        imgsz=640,  # training image size
        device=torch.device("cpu"), #torch.device("cuda" if torch.cuda.is_available() else "cpu"),  # device to run on, i.e. device=0 or device=0,1,2,3 or device=cpu
        project="ultralytics_output",
        name="third_attempt",
        plots=True,
        lr0=0.005,
        lrf=0.1,
        dropout=0.001,
        val = True
        # resume=True # check if this is the right parameter to set to True
    )

    # Val
    # Evaluate model performance on the validation set
    metrics = model.val(plots=True)
    print(metrics.box.map)  # map50-95
    print(metrics.box.map50)  # map50
    print(metrics.box.map75)  # map75
    print(metrics.box.maps)  # a list contains map50-95 of each category

    # Perform object detection on an image
    results = model('dataset/images/val/00000.jpg')
    results[0].show()

    # Export the model to ONNX format
    path = model.export(format="onnx")  # return path to exported model