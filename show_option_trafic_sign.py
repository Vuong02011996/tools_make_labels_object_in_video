import cv2
import numpy as np
import os
import sys

size_image = 50
num_col = 4
class_id = None


def onMouse(event, x, y, flags, param):
    global class_id
    if event == cv2.EVENT_LBUTTONDOWN:
        print('x = %d, y = %d' % (x, y))
        for index in range(7):
            id_next = index + 1
            if index * size_image < y < id_next * size_image:
                for i in range(num_col):
                    i_next = i + 1
                    if i * size_image < x < i_next * size_image:
                        print('class id = ', i + index * num_col)
                        class_id = i + index * num_col


def load_image_bbgt_to_list():
    path_image = './bbgt/'
    list_files_image = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path_image):
        for file in f:
            if '.png' in file:
                list_files_image.append(os.path.join(r, file))
    return list_files_image


def label_window():
    list_files_image = load_image_bbgt_to_list()
    list_files_image.sort()
    main_title_window = 'Test'

    flag_run_file_label = True
    while flag_run_file_label:
        img = cv2.imread(list_files_image[0])
        img = cv2.resize(img, (size_image, size_image), interpolation=cv2.INTER_AREA)
        numpy_horizontal_concat = img
        for i in range(1, len(list_files_image)):
            img = cv2.imread(list_files_image[i])
            img = cv2.resize(img, (size_image, size_image), interpolation=cv2.INTER_AREA)
            if i < num_col:
                numpy_horizontal_concat = np.concatenate((numpy_horizontal_concat, img), axis=1)
            if i == num_col:
                numpy_horizontal_concat1 = img
            if i > num_col and (i < num_col * 2):
                numpy_horizontal_concat1 = np.concatenate((numpy_horizontal_concat1, img), axis=1)
            if i == num_col * 2:
                numpy_horizontal_concat2 = img
            if i > num_col * 2 and (i < num_col * 3):
                numpy_horizontal_concat2 = np.concatenate((numpy_horizontal_concat2, img), axis=1)
            if i == num_col * 3:
                numpy_horizontal_concat3 = img
            if i > num_col * 3 and (i < num_col * 4):
                numpy_horizontal_concat3 = np.concatenate((numpy_horizontal_concat3, img), axis=1)
            if i == num_col * 4:
                numpy_horizontal_concat4 = img
            if i > num_col * 4 and (i < num_col * 5):
                numpy_horizontal_concat4 = np.concatenate((numpy_horizontal_concat4, img), axis=1)
            if i == num_col * 5:
                numpy_horizontal_concat5 = img
            if i > num_col * 5 and (i < num_col * 6):
                numpy_horizontal_concat5 = np.concatenate((numpy_horizontal_concat5, img), axis=1)
            if i == num_col * 6:
                numpy_horizontal_concat6 = img
            if i > num_col * 6:
                numpy_horizontal_concat6 = np.concatenate((numpy_horizontal_concat6, img), axis=1)

            if i == 26:
                img = np.zeros_like(img)
                # img = cv2.resize(img, (size_image, size_image), interpolation=cv2.INTER_AREA)
                numpy_horizontal_concat6 = np.concatenate((numpy_horizontal_concat6, img), axis=1)

        combine_image = np.concatenate((numpy_horizontal_concat, numpy_horizontal_concat1, numpy_horizontal_concat2
                                        , numpy_horizontal_concat3, numpy_horizontal_concat4
                                        , numpy_horizontal_concat5, numpy_horizontal_concat6), axis=0)
        cv2.namedWindow(main_title_window, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(main_title_window, combine_image)
        cv2.setMouseCallback(main_title_window, onMouse)
        cv2.waitKey()
        if class_id is not None:
            cv2.destroyWindow(main_title_window)
            break


if __name__ == "__main__":
    label_window()

    '''
    + This module return toa do cua cac anh bien bao dung cho chon loai bien bao.
    + click image => toa do => save id class
    '''
