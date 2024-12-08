import os
import shutil
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

def move_images(source_dir, target_dir, file_extension=".png"):
    # Check if source and target directories exist
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        return
    if not os.path.exists(target_dir):
        print(f"Target directory '{target_dir}' does not exist. Creating it now.")
        os.makedirs(target_dir)
        train_images_path = os.path.join(target_dir, "train")
        val_images_path = os.path.join(target_dir, "val")
        os.makedirs(train_images_path, exist_ok=True)
        os.makedirs(val_images_path, exist_ok=True)

    split_file_train = "c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/splits/train.txt"
    split_file_test = "c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/splits/test.txt"
    
    # Loop through all files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the file has the specified image extension
        if filename.lower().endswith(file_extension):

            number_to_find = remove_leading_zeros("".join(filter(str.isdigit, filename)))
            if is_number_in_file(split_file_train, number_to_find):
                train_or_val = "train"
            elif is_number_in_file(split_file_test, number_to_find):
                train_or_val = "val"
            else:
                train_or_val = ""
            # Construct full file paths
            source_file = os.path.join(source_dir, filename)

            target_file = os.path.join(target_dir, train_or_val, filename)
            
            # Move the file
            try:
                shutil.move(source_file, target_file)
                print(f"Moved: {filename}")
            except Exception as e:
                print(f"Error moving {filename}: {e}")
        else:
            print(f"Skipping non-image file: {filename}")

# Example usage
source_directory = 'c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/Town01_Opt_120_depth/Town01_Opt_120/ClearNoon/height20m/depth'  # Replace with your source folder path
target_directory = 'c:/Users/chase/OneDrive/Documents/Grad/ML_for_Robots/final_project/dataset/depth'  # Replace with your target folder path
image_extension = ".png"  # You can change this to ".png" or other image formats

move_images(source_directory, target_directory, image_extension)
