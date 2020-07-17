import os
import cv2
import shutil
import numpy as np

NAME_TRAFIC_SIGN = ["Cam dung va do xe", "Cam do xe", "Cam bop coi", "Cam xe tai",
                    "Cam xe tai tu 2,5 tan", "Cam re trai", "Cam re phai",
                    "Cam do xe ngay le", "Cam do xe ngay chan",
                    "Cam di nguoc chieu", "Han che trong luong xe",
                    "Toc do toi da cho phep", "Nguoi di bo cat ngang", "Tre em",
                    "Giao nhau voi duong uu tien", "Cho ngoat nguy hiem",
                    "Noi giao nhau cua duong dong cap",
                    "Giao nhau voi duong khong uu tien", "Di cham",
                    "Duong di thang phai theo", "Cho", "Diem dung xe buyt",
                    "Tram xang", "Chi huong duong", "Benh vien", "Duong di bo",
                    "Noi do xe"]


def get_all_file_image_and_label():
    path_image = '/home/vuong/Videos/17:07:37220898/image_left/'
    path_label = '/home/vuong/Videos/17:07:37220898/label_left/'

    list_files_image = []
    list_files_label = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path_image):
        for file in f:
            if '.jpg' in file:
                list_files_image.append(os.path.join(r, file))
    for r, d, f in os.walk(path_label):
        for file in f:
            if '.txt' in file:
                list_files_label.append(os.path.join(r, file))
    return list_files_image, list_files_label


def show_label_select():
    list_files_image, list_files_label = get_all_file_image_and_label()
    list_files_label.sort()
    list_files_image.sort()
    for i in range(len(list_files_image)):
        image_file = list_files_image[i]
        label_file = list_files_label[i]
        img = cv2.imread(image_file)
        (H, W) = img.shape[:2]
        print('label_file', label_file)
        with open(label_file) as fr:
            lines = fr.readlines()
            print(lines)
            print(len(lines))
            for line in lines:
                class_id = int(float(line.split(' ')[0]))
                x = int(float(line.split(' ')[1]) * W)
                y = int(float(line.split(' ')[2]) * H)
                w = int(float(line.split(' ')[3]) * W)
                h = int(float(line.split(' ')[4]) * H)

                # x = int(float(line.split(' ')[1]))
                # y = int(float(line.split(' ')[2]))
                # w = int(float(line.split(' ')[3]))
                # h = int(float(line.split(' ')[4]))

                print('x, y, w, h ', x, y, w, h)
                # [('Tram dung xe buyt', [(685, 182), (724, 182), (724, 245), (685, 245)], None, None, False),
                # ('Giao nhau voi duong khong uu tien', [(412, 141), (442, 141), (442, 164), (412, 164)], None, None, False)]
                print(
                    '[({}, [({}, {}), ({}, {}), ({}, {}), ({}, {})]'.format(NAME_TRAFIC_SIGN[class_id], x, y, x + w, y,
                                                                            0, 0, y, y + h))

                crop_img = img[y - int(h / 2):y + int(h / 2), x - int(w / 2):x + int(w / 2)]
                cv2.imshow("image", img)
                cv2.imshow("cropped", crop_img)
                cv2.waitKey(0)
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord("q"):
        #     break


def copy_file_image_and_label_with_class_id(class_id_compare):
    list_files_image, list_files_label = get_all_file_image_and_label()
    list_files_label.sort()
    list_files_image.sort()

    path_class_id_image = '/home/vuong/Pictures/BBGT/image/'
    path_class_id_label = '/home/vuong/Pictures/BBGT/label/'
    if os.path.exists(path_class_id_label) and os.path.exists(path_class_id_image):
        shutil.rmtree(path_class_id_label)
        shutil.rmtree(path_class_id_image)

    if not os.path.isdir(path_class_id_image):
        os.makedirs(path_class_id_image)

    if not os.path.isdir(path_class_id_label):
        os.makedirs(path_class_id_label)

    for i in range(len(list_files_image)):
        image_file = list_files_image[i]
        label_file = list_files_label[i]
        if image_file.split('.')[1] != label_file.split('.')[1]:
            list_files_label = np.asarray(list_files_label)
            list_files_image = np.asarray(list_files_image)
            a  = 0
        list_class_id = []
        with open(label_file) as fr:
            lines = fr.readlines()

            for line in lines:
                class_id = int(float(line.split(' ')[0]))
                list_class_id.append(class_id)

        if class_id_compare in list_class_id:
            print(class_id_compare)
            print(list_class_id)
            print(image_file)
            print(label_file)
            shutil.copy2(image_file, path_class_id_image)
            shutil.copy2(label_file, path_class_id_label)
            # a = 0
            # img = cv2.imread(image_file)
            # cv2.imshow("image", img)
            # cv2.waitKey(0)


if __name__ == "__main__":
    copy_file_image_and_label_with_class_id(class_id_compare=2)
    # show_label_select()
