

''' This script is to train yolov8 traing. Before training change the working directory 
    such that the runs folder which is created during the training of yolov8 gets saved'''


# Import necessary libraries
from IPython import display
import ultralytics
from ultralytics import YOLO

# Check Ultralytics installation
ultralytics.checks()
# Initialize YOLO object
yolo = YOLO()

# Set YOLO training parameters
task = 'detect'
mode = 'train'
model = 'Disease_Model_3.pt'
data = 'dataset.yaml'
epochs = 400
imgsz = 1280
save = True
patience = 100

# Train YOLO model
yolo.train(epochs=epochs, imgsz=imgsz, task=task, model=model, data=data, save=save, patience=patience)
