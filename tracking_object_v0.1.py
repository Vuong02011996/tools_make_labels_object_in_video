# import the necessary packages
from imutils.video import FPS
import imutils
import os
import cv2
import shutil
import time
import show_option_trafic_sign
import define


def on_pos_video_trackbar(val):
    global vs, frame_index

    if val != frame_index:
        frame_index = val
        vs.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        print("Set Pos : ", val)


#  function called by trackbar, sets the speed of playback
def setSpeed(val):
    global playSpeed
    playSpeed = max(val, 1)


def mouse_callback(event, x, y, flags, param):
    global mouse_down
    global step

    if event == cv2.EVENT_LBUTTONDOWN:
        if mouse_down is False:
            mouse_down = True
            step = 0
        else:
            step += 1

    elif event == cv2.EVENT_LBUTTONUP and mouse_down:
        mouse_down = False


main_title_window = "Video"
frame_index = 0
playSpeed = 250
mouse_down = False
step = 0

path_video = define.path_video
path_save_data = define.path_save_data
name_video = define.name_video

vs = cv2.VideoCapture(path_video)
if vs.isOpened() is False:
    print("Open video false")
    exit()
num_of_frame = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
pos_slider_max = num_of_frame
cv2.namedWindow(main_title_window, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(main_title_window, mouse_callback)
cv2.createTrackbar('Position', main_title_window, 0, pos_slider_max, on_pos_video_trackbar)
cv2.createTrackbar("Speed", "Video", playSpeed, 500, setSpeed)


def main():
    global frame_index
    global step

    # Initial tracker video
    tracker_type = "csrt"  # csrt
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create,  # higher object tracking accuracy and can tolerate slower FPS throughput
        "kcf": cv2.TrackerKCF_create,  # faster FPS throughput but can handle slightly lower object tracking accuracy
        "boosting": cv2.TrackerBoosting_create,
        "mil": cv2.TrackerMIL_create,
        "tld": cv2.TrackerTLD_create,
        "medianflow": cv2.TrackerMedianFlow_create,
        "mosse": cv2.TrackerMOSSE_create
    }
    tracker = OPENCV_OBJECT_TRACKERS[tracker_type]()
    # initialize the bounding box coordinates of the object we are going
    # to track
    initBB = None

    fps = None
    start = True
    view_left = False
    view_right = False
    # loop for choice view left or right
    ret, frame_ori = vs.read()
    print("Please press r(R) to view right window or e(E) to view left side window!")
    while start:
        view_frame = imutils.resize(frame_ori, width=1000)
        text = 'Please press r(R) to view right window or e(E) to view left side window!'
        (H, W) = view_frame.shape[:2]
        cv2.putText(view_frame, text, (10, H - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imshow(main_title_window, view_frame)

        key = cv2.waitKey(playSpeed) & 0xFF
        if key == ord("e") or key == ord("E"):
            folder_image = path_save_data + '/image_left/'
            folder_label = path_save_data + '/label_left/'

            if os.path.exists(folder_image) and os.path.exists(folder_label):
                shutil.rmtree(folder_image)
                shutil.rmtree(folder_label)
            if not os.path.exists(folder_image):
                os.makedirs(folder_image)
            if not os.path.exists(folder_label):
                os.makedirs(folder_label)
            start = False
            view_left = True
        elif key == ord("r") or key == ord("R"):
            folder_image = path_save_data + '/image_right/'
            folder_label = path_save_data + '/label_right/'

            if os.path.exists(folder_image) and os.path.exists(folder_label):
                shutil.rmtree(folder_image)
                shutil.rmtree(folder_label)
            if not os.path.exists(folder_image):
                os.makedirs(folder_image)
            if not os.path.exists(folder_label):
                os.makedirs(folder_label)
            start = False
            view_right = True

    # loop over frames from the video stream
    while True:
        vs.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame_ori = vs.read()
        (H_ori, W_ori) = frame_ori.shape[:2]
        if view_left:
            x_max_show = 1850
            y_max_show = 900
            x_min_show = 0
            y_min_show = 0
            frame = frame_ori[:int(H_ori), :int(W_ori / 2)]
        elif view_right:
            x_max_show = 3800
            y_max_show = 900
            x_min_show = 1920
            y_min_show = 0
            frame = frame_ori[:int(H_ori), int(W_ori / 2):]

        view_frame = frame_ori[y_min_show:y_max_show, x_min_show:x_max_show]

        frame_index += 1
        cv2.setTrackbarPos('Position', main_title_window, frame_index)

        if mouse_down:
            step += 1
        # check to see if we have reached the end of the stream
        if frame is None:
            break

        (H, W) = frame.shape[:2]

        # check to see if we are currently tracking an object
        if initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(frame)
            if success:
                (x, y, w, h) = [int(v) for v in box]
                if (x + w) > 1900 or x < 5 or y > 900 or y < 0:
                    initBB = None
                    show_option_trafic_sign.class_id = None
                    tracker.clear()
                else:
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  (0, 255, 0), 2)
                    print('tracking success! x, y, w, h = ', x, y, w, h)
                    # format (class_id xcen ycen w h)
                    x_cen = x + (w / 2)
                    y_cen = y + (h / 2)
                    boding_box_label = str(show_option_trafic_sign.class_id) + ' ' + str(x_cen / W) + ' ' + str(
                        y_cen / H) + ' ' + str(
                        w / W) + ' ' + str(h / H) + '\n'

                    label_file = os.path.join(folder_label, name_video + "." + str(frame_index) + ".txt")
                    image_file = os.path.join(folder_image, name_video + "." + str(frame_index) + ".jpg")
                    '''check file existed create new file for new object'''
                    while os.path.exists(label_file) and os.path.exists(image_file):
                        label_file = label_file.split('.')[0] + "_obj"
                        image_file = image_file.split('.')[0] + "_obj"
                        label_file = label_file + "." + str(frame_index) + ".txt"
                        image_file = image_file + "." + str(frame_index) + ".jpg"

                    f_label_image_write = open(label_file, 'w')
                    f_label_image_write.write(boding_box_label)

                    cv2.imwrite(image_file, frame)

            fps.update()
            fps.stop()
            info = [
                ("Tracker", tracker_type),
                ("Success", "Yes" if success else "No"),
                ("FPS", "{:.2f}".format(fps.fps())),
            ]
            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # show the output frame
        # H, W 1080 3840
        cv2.imshow(main_title_window, view_frame)
        key = cv2.waitKey(playSpeed) & 0xFF
        if key == ord("d") or key == ord("D"):
            initBB = None
            show_option_trafic_sign.class_id = None
            tracker.clear()
        elif key == ord("s") or key == ord("S"):
            initBB = None
            show_option_trafic_sign.class_id = None
            tracker.clear()
            while initBB is None:
                tracker = OPENCV_OBJECT_TRACKERS[tracker_type]()
                initBB = cv2.selectROI(main_title_window, frame, fromCenter=False,
                                       showCrosshair=True)
            if sum(initBB) == 0:
                initBB = None
                continue
            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            while show_option_trafic_sign.class_id is None:
                show_option_trafic_sign.label_window()

            tracker.init(frame, initBB)
            fps = FPS().start()
        elif key == ord("c") or key == ord("C"):
            path_image_cp = folder_image + '_cp_' + str(frame_index) + '/'
            path_label_cp = folder_image + '_cp_' + str(frame_index) + '/'
            shutil.copytree(folder_image, path_image_cp)
            shutil.copytree(folder_label, path_label_cp)
        elif key == ord("h") or key == ord("H"):
            while True:
                view_frame_help = imutils.resize(frame, width=1000)
                (H, W) = view_frame_help.shape[:2]
                info = [
                    ("Press q or Q", "to quit program"),
                    ("Press h or H", "view help"),
                    ("Press c or C", "copy image data current to another folder"),
                    ("Press g or G", "decrease 2 frame (Don't press while tracking)"),
                    ("Press f or F", "increase 2 frame (Don't press while tracking)"),
                    ("Press d or D", "delete bounding box of the object"),
                    ("Press s or S", "select the bounding box of the object we want to track"),
                    ("Press h or H", "to quit help"),
                ]
                # loop over the info tuples and draw them on our frame
                for (i, (k, v)) in enumerate(info):
                    text = "{}: {}".format(k, v)
                    cv2.putText(view_frame_help, text, (10, H - ((i * 20) + 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                cv2.imshow(main_title_window, view_frame_help)
                key = cv2.waitKey(playSpeed) & 0xFF
                if key == ord("h") or key == ord("H"):
                    break

        elif key == ord("f") or key == ord("F"):
            if frame_index > 2:
                frame_index -= 4
            print('frame_index', frame_index)
        elif key == ord("g") or key == ord("G"):
            if frame_index < num_of_frame:
                frame_index += 4
            print('frame_index', frame_index)
        elif key == ord("p") or key == ord("P"):
            while True:
                view_frame_help = imutils.resize(frame, width=1000)
                cv2.imshow(main_title_window, view_frame_help)
                key = cv2.waitKey(0) & 0xFF
                if key == ord("p") or key == ord("P"):
                    break

                time.sleep(1)

        elif key == ord("q") or key == ord("Q"):
            break

    vs.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
    '47400'
