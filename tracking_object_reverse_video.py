# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import os
import cv2
import shutil
import time
import show_option_trafic_sign
import define


def on_pos_video_trackbar(val):
    global vs, frame_idx

    if val != frame_idx:
        frame_idx = val
        vs.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
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
playSpeed = 250
mouse_down = False
step = 0

path_video = define.path_video
path_save_data = define.path_save_data

vs = cv2.VideoCapture(path_video)
num_of_frame = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
pos_slider_max = num_of_frame
cv2.namedWindow(main_title_window, cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback(main_title_window, mouse_callback)
cv2.createTrackbar('Position', main_title_window, 0, pos_slider_max, on_pos_video_trackbar)
cv2.createTrackbar("Speed", "Video", playSpeed, 500, setSpeed)


# window_show = "List image"
# cv2.namedWindow(window_show, cv2.WINDOW_AUTOSIZE)


def main():
    global frame_idx
    global step

    folder_image = path_save_data + '/image/'
    folder_label = path_save_data + '/label/'

    shutil.rmtree(folder_image)
    shutil.rmtree(folder_label)
    if not os.path.exists(folder_image):
        os.makedirs(folder_image)
    if not os.path.exists(folder_label):
        os.makedirs(folder_label)

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
    count_save = 0
    # loop over frames from the video stream

    frame_idx = int(vs.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
    while frame_idx >= 0:
        # Set the current frame position to start:
        vs.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)

        ret, frame_ori = vs.read()
        frame_idx = frame_idx - 1

        cv2.setTrackbarPos('Position', main_title_window, frame_idx)

        if mouse_down:
            step += 1
        # check to see if we have reached the end of the stream
        if frame_ori is None:
            break

        # frame = imutils.resize(frame_ori, width=2000)
        frame = cv2.resize(frame_ori, (0, 0), fx=0.5, fy=0.5)
        # frame = frame_ori
        (H, W) = frame.shape[:2]

        # check to see if we are currently tracking an object
        if initBB is not None:
            # grab the new bounding box coordinates of the object
            (success, box) = tracker.update(frame)
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h),
                              (0, 255, 0), 2)
                if x > 0 and y > 0:
                    print('tracking success! x, y, w, h = ', x, y, w, h)
                    boding_box_label = str(show_option_trafic_sign.class_id) + ' ' + str(x / W) + ' ' + str(y / H) + ' ' + str(
                        w / W) \
                                       + ' ' + str(h / H)

                    label_image_file = open(os.path.join(folder_label, name_video + "_" + str(count_save) + ".txt"),
                                            'a')
                    label_image_file.write(boding_box_label)
                    cv2.imwrite(os.path.join(folder_image, name_video + "_" + str(count_save) + ".jpg"),
                                frame)
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
        cv2.imshow(main_title_window, frame)
        key = cv2.waitKey(playSpeed) & 0xFF
        if key == ord("s") or key == ord("S"):
            # select the bounding box of the object we want to track (make
            # sure you press ENTER or SPACE after selecting the ROI)
            tracker.clear()
            tracker = OPENCV_OBJECT_TRACKERS[tracker_type]()
            initBB = cv2.selectROI(main_title_window, frame, fromCenter=False,
                                   showCrosshair=True)
            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            while Test_show_image.class_id is None:
                print(Test_show_image.class_id)
                Test_show_image.label_window()

            print(Test_show_image.class_id)
            tracker.init(frame, initBB)
            fps = FPS().start()
        elif key == ord("d") or key == ord("D"):
            initBB = None
            Test_show_image.class_id = None
            tracker.clear()
            while initBB is None:
                tracker = OPENCV_OBJECT_TRACKERS[tracker_type]()
                initBB = cv2.selectROI(main_title_window, frame, fromCenter=False,
                                       showCrosshair=True)
            # start OpenCV object tracker using the supplied bounding box
            # coordinates, then start the FPS throughput estimator as well
            while Test_show_image.class_id is None:
                print(Test_show_image.class_id)
                Test_show_image.label_window()

            print(Test_show_image.class_id)
            tracker.init(frame, initBB)
            fps = FPS().start()
        elif key == ord("a") or key == ord("A"):
            initBB = None
            Test_show_image.class_id = None
            tracker.clear()

        elif key == ord("q") or key == ord("Q"):
            break

        count_save += 1
        # time.sleep(0.01)

    vs.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

    '''A Truong Don ban ve cho cu'''
