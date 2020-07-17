import cv2
import os
import numpy as np
import shutil
from define import path_save_data, path_file_classes


def combine_file_the_same_base_name(view_choice='left'):
    path_image = path_save_data + '/image_' + view_choice + '/'
    path_label = path_save_data + '/label_' + view_choice + '/'
    path_image_cp = path_save_data + '/image_' + view_choice + '_cp/'
    path_label_cp = path_save_data + '/label_' + view_choice + '_cp/'
    if os.path.exists(path_image_cp) and os.path.exists(path_label_cp):
        shutil.rmtree(path_image_cp)
        shutil.rmtree(path_label_cp)
    print('copy folder process....')
    shutil.copytree(path_image, path_image_cp)
    shutil.copytree(path_label, path_label_cp)

    # take file base name based on frame index
    list_index_frame = []
    for r, d, f in os.walk(path_image):
        for file in f:
            if '.jpg' in file:
                list_index_frame.append(file.split('.')[1])
    list_index_frame = np.asarray(list_index_frame, dtype=int)
    array_frame_index, indices = np.unique(list_index_frame, return_inverse=True)

    for idex_frame in array_frame_index:

        list_files_image = []
        list_files_label = []

        # r=root, d=directories, f = files
        # take group file name the same frame index
        for r, d, f in os.walk(path_image):
            for file in f:
                if '.' + str(idex_frame) + '.jpg' in file:
                    list_files_image.append(os.path.join(r, file))
        for r, d, f in os.walk(path_label):
            for file in f:
                if '.' + str(idex_frame) + '.txt' in file:
                    list_files_label.append(os.path.join(r, file))
        list_files_label.sort()
        list_files_image.sort()
        # Only process for image more than one object.
        if len(list_files_image) > 1:
            image_file_0 = list_files_image[0]
            img = cv2.imread(image_file_0)
            (H, W) = img.shape[:2]
            label_file_0 = list_files_label[0]

            # process each group file the same frame index: draw rectangle to img and combine bounding box
            for i in range(1, len(list_files_image)):
                label_file = list_files_label[i]
                # print('H, W', H, W)
                with open(label_file) as fr:
                    lines = fr.readlines()
                    print(lines)
                    print(len(lines))
                    for line in lines:
                        # str(float(line.split(' ')[4])) remove /n in end line.
                        class_id = int(float(line.split(' ')[0]))
                        x_cen = line.split(' ')[1]
                        y_cen = line.split(' ')[2]
                        w = line.split(' ')[3]
                        h = line.split(' ')[4]
                        boding_box_label = line.split(' ')[0] + ' ' + x_cen + ' ' + y_cen + ' ' \
                                           + w + ' ' + str(float(h)) + '\n'

                        x_min = float(x_cen) - (float(w) / 2)
                        y_min = float(y_cen) - (float(h) / 2)

                        x_min = int(x_min * W)
                        y_min = int(y_min * H)
                        w = int(float(w) * W)
                        h = int(float(h) * H)
                        cv2.rectangle(img, (x_min, y_min), (x_min + w, y_min + h),
                                      (0, 255, 0), 2)
                with open(label_file_0, 'a') as f_label_image_write:
                    f_label_image_write.write(boding_box_label)
            # cv2.imshow("image", img)
            # cv2.waitKey(0)
            cv2.imwrite(image_file_0, img)

    # remove all file have obj in file
    for r, d, f in os.walk(path_image):
        for file in f:
            if '_obj' in file:
                os.remove(os.path.join(r, file))
    for r, d, f in os.walk(path_label):
        for file in f:
            if '_obj' in file:
                os.remove(os.path.join(r, file))

    "copy file classes.txt to folder label for labelImg tool"
    if not os.path.exists(path_file_classes):
        shutil.copy2(path_file_classes, path_label)


if __name__ == "__main__":
    combine_file_the_same_base_name()
