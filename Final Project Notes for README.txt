Notes for ML for Robots final project implementation:

PART 1
* First, run the move_images.py file after downloading the dataset to get the images in the yolo format
* Next, run the fix_bboxes.py script, once with the "split" argument sent to "train" and once with it set to "test"
* convert_json.py file is deprecated
* There are actually only 9 classes, not 28
* When converting bboxes, if no valid bboxes are found, a label script is written with the correct title for the image, but empty
* Some of the images seem to have duplicate labels, probably because I deleted the image folders before the fix_bboxes.py script finished while testing. However, the ultralytics code seems to handle this by removing duplicate labels