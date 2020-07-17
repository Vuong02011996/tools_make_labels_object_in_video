# Tools make labels object in video with tracking

## Requirements
opencv-python

## How to using tools make labels object in video with tracking 
* Change directory video and file save data in module define.py
* Run `python3 tracking_object_v0.1.py` in terminal
* Press key h or H to view help using tools.
* After make label all video, you can combine the same frame with many object to only a frame by:
    `python3 combine_image_many_object.py`

## Check result data set after make labels for object
* After made label for frame you can check result by using 
tool labelImg in repo https://github.com/tzutalin/labelImg
* After clone repo to PC you can run command below to check.
`python3 labelImg.py ./image_right ./label_right/classes.txt`