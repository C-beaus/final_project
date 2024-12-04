import json
import os
import re

def is_number_in_file(file_path, number_to_find):
    pattern = r'\b' + re.escape(str(number_to_find)) + r'\b'  # \b ensures it's a whole word match
    with open(file_path, 'r') as file:
        for line in file:
            if re.search(pattern, line):
                return True
    return False

def remove_leading_zeros(s):
    # Remove leading zeros, but return '0' if the string is empty or only zeroes
    if s == "0" or s.lstrip('0') == '':
        return "0"
    return s.lstrip('0')

# Parameters
input_dir = "c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/Town01_Opt_120_color/Town01_Opt_120/ClearNoon/bboxes"
output_dir = "c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/dataset/labels/testing"
image_width = 1920  # Replace with your image width
image_height = 1080  # Replace with your image height

split_file_train = "c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/splits/train.txt"
split_file_test = "c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/splits/test.txt"


# input_dir = "c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/Town01_Opt_120_color/Town01_Opt_120/ClearNoon/bboxes"
# output_dir = "path/to/output/labels"
os.makedirs(output_dir, exist_ok=True)
train_dir = os.path.join(output_dir, "train")
val_dir = os.path.join(output_dir, "val")
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
# output_dir = os.path.join(output_dir, "labels")
# os.makedirs(output_dir, exist_ok=True)

# Process each JSON file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):  # Ensure only JSON files are processed
        input_json = os.path.join(input_dir, filename)
        with open(input_json, 'r') as file: # Load JSON data
            data = json.load(file)
            print(f"Processing file: {input_json}")

        number_to_find = remove_leading_zeros("".join(filter(str.isdigit, filename)))
        if is_number_in_file(split_file_train, number_to_find):
            train_or_val = "train"
        elif is_number_in_file(split_file_test, number_to_find):
            train_or_val = "val"
        else:
            train_or_val = ""
        
        save_file_name = "".join(filter(str.isdigit, filename))
        save_file_name = os.path.join(train_or_val, save_file_name)

        # Process each object in JSON
        for obj in data:
            corners = obj["corners"]
            class_id = obj["class"][0]  # Extract class ID

            # Extract x, y coordinates from corners
            x_coords = [corner[0] for corner in corners]
            y_coords = [corner[1] for corner in corners]

            # my_list = [1, 2, 2, 3, 4, 4, 5]
            # unique_list = list(dict.fromkeys(my_list))
            # print(unique_list)  # Output: [1, 2, 3, 4, 5]

            # x_coords = list(dict.fromkeys(x_coords))
            # y_coords = list(dict.fromkeys(y_coords))


            # Calculate 2D bounding box
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)

            # # handle bboxes that are out of frame
            # if x_min < 0:
            #     x_min = 0
            # if y_min < 0:
            #     y_min = 0

            # if max values are not greater than zero, skip bbox
            # if round(y_max) > 0 & round(x_max) > 0:
                # Convert to YOLO format (normalized)
            x_center = ((x_min + x_max) / 2) / image_width
            y_center = ((y_min + y_max) / 2) / image_height
            width = (x_max - x_min) / image_width
            height = (y_max - y_min) / image_height

            # Create YOLO annotation string
            yolo_annotation = f"{class_id} {x_center} {y_center} {width} {height}\n"

            # Save to corresponding file
            output_file = os.path.join(output_dir, save_file_name + ".txt")
            with open(output_file, 'a') as label_file:
                label_file.write(yolo_annotation)

print("Conversion complete. Annotations saved to:", output_dir)

