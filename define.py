path_video = '/home/vuong/Videos/16:31:47.063371.mp4'
name_video = path_video.split('/')[-1].split('.')[0] + path_video.split('/')[-1].split('.')[1]
path_save_data = '/home/vuong/Videos/' + name_video
path_file_classes = 'classes.txt'


'''
Train custom object: darknet.exe detector train data/obj.data yolo-obj.cfg yolov4.conv.137
train 2 class truoc.(Cam dung va do xe vs Cam do xe)

B1. Copy file .cfg and change 8 option:
    + batch
    + subdivisions
    + max_batches
    + steps to 80% and 90% of max_batches
    + network size width=416 height=416 or any value multiple of 32
    + line classes=80 to your number of objects (in each of 3 layer)
    + change [filters=255] to filters=(classes + 5)x3 in the 3 [convolutional] before each [yolo] layer
B2. Create file obj.data in the directory build\darknet\x64\data\
        classes= 2
        train  = data/train.txt
        valid  = data/test.txt
        names = data/obj.names
        backup = backup/
    + Create file obj.names the same file class.txt and put to the directory build\darknet\x64\data\
    + Create file train.txt and test.txt and put to the directory build\darknet\x64\data\
        data/obj/img1.jpg
        data/obj/img2.jpg
        data/obj/img3.jpg
        ....
B3. Download pre-trained weights for the convolutional layers and put to the directory build\darknet\x64 
'''