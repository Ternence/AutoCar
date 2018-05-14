import string

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle

import serial
import time
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera

from car import*

from combined_thresh import combined_thresh
from perspective_transform import perspective_transform
from Line import Line
from line_fit import line_fit, tune_fit, final_viz, calc_curve, calc_vehicle_offset
from moviepy.editor import VideoFileClip

# Global variables (just to make the moviepy video annotation work)
with open('calibrate_camera.p', 'rb') as f:
    save_dict = pickle.load(f)
mtx = save_dict['mtx']
dist = save_dict['dist']
window_size = 5  # how many frames for line smoothing
left_line = Line(n=window_size)
right_line = Line(n=window_size)
detected = False  # did the fast line fit detect the lines?
left_curve, right_curve = 0., 0.  # radius of curvature for left and right lanes
left_lane_inds, right_lane_inds = None, None  # for calculating curvature


# MoviePy video annotation will call this function
def annotate_image(img_in):
    """
    Annotate the input image with lane line markings
    Returns annotated image
    """
    global mtx, dist, left_line, right_line, detected
    global left_curve, right_curve, left_lane_inds, right_lane_inds

    # Undistort, threshold, perspective transform
    undist = img_in
    # undist = cv2.undistort(img_in, mtx, dist, None, mtx)
    img, abs_bin, mag_bin, dir_bin, hls_bin = combined_thresh(undist)
    binary_warped, binary_unwarped, m, m_inv = perspective_transform(img)

    # Perform polynomial fit
    print(detected)
    if not detected:
        # Slow line fit
        ret = line_fit(binary_warped)
        if ret is not None:
            left_fit = ret['left_fit']
            right_fit = ret['right_fit']
            nonzerox = ret['nonzerox']
            nonzeroy = ret['nonzeroy']
            left_lane_inds = ret['left_lane_inds']
            right_lane_inds = ret['right_lane_inds']

            # Get moving average of line fit coefficients
            left_fit = left_line.add_fit(left_fit)
            right_fit = right_line.add_fit(right_fit)

            # Calculate curvature
            left_curve, right_curve = calc_curve(left_lane_inds, right_lane_inds, nonzerox, nonzeroy)

            detected = True  # slow line fit always detects the line

    else:  # implies detected == True
        # Fast line fit
        left_fit = left_line.get_fit()
        right_fit = right_line.get_fit()
        ret = tune_fit(binary_warped, left_fit, right_fit)
        if ret is not None:
            left_fit = ret['left_fit']
            right_fit = ret['right_fit']
            nonzerox = ret['nonzerox']
            nonzeroy = ret['nonzeroy']
            left_lane_inds = ret['left_lane_inds']
            right_lane_inds = ret['right_lane_inds']

            # Only make updates if we detected lines in current frame
            left_fit = ret['left_fit']
            right_fit = ret['right_fit']
            nonzerox = ret['nonzerox']
            nonzeroy = ret['nonzeroy']
            left_lane_inds = ret['left_lane_inds']
            right_lane_inds = ret['right_lane_inds']

            left_fit = left_line.add_fit(left_fit)
            right_fit = right_line.add_fit(right_fit)
            left_curve, right_curve = calc_curve(left_lane_inds, right_lane_inds, nonzerox, nonzeroy)
            detected = True
        else:
            detected = False

    vehicle_offset = calc_vehicle_offset(undist, left_fit, right_fit)

    distance = get_distance()
    set_speed(TURN_LEFT,)
    set_turn()

    # Perform final visualization on top of original undistorted image
    result = final_viz(undist, left_fit, right_fit, m_inv, left_curve, right_curve, vehicle_offset)

    return result

#
# def commonControl(vehicle_offset):
#     ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
#     start = time.clock()
#     end = time.clock()
#     print('duty cycle is %s' % (end - start))
#     start = time.clock()
#     response = ser.readline()
#     s_r = response
#     temp = s_r.split(":")
#     temp = temp[1].split(",")
#     power = string.atof(temp[0])
#     left_speed = string.atof(temp[1])
#     right_speed = string.atof(temp[2])
#     sonar = string.atof(temp[3].strip())
#     print('msg is %f %f %f %f' % (power, left_speed, right_speed, sonar))
#     # global power, radius
#     #
#     # radius = vehicle_offset * 0.5
#     ser.write('RASPI: %s, %s\n' % ('50.0', vehicle_offset))
#     sys.argv[1], sys.argv[2]
#     time.sleep(0.03)


def annotate_video(input_file, output_file):
    """ Given input_file video, save annotated video to output_file """
    video = VideoFileClip(input_file)
    annotated_video = video.fl_image(annotate_image)
    annotated_video.write_videofile(output_file, audio=False)


if __name__ == '__main__':
    # Annotate the video
    # annotate_video('project_video1.mp4', 'out1.mp4')
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    time.sleep(0.1)

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # show the frame
        cv2.imshow("Frame", image)

        resultImage = annotate_image(image)

        key = cv2.waitKey(1) & 0xFF

        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break



# Show example annotated image on screen for sanity check
# img_file = 'test_images/test2.jpg'
# img = mpimg.imread(img_file)
# result = annotate_image(img)
# result = annotate_image(img)
# result = annotate_image(img)
# plt.imshow(result)
# plt.show()
