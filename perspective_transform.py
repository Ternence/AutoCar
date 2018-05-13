import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
from combined_thresh import combined_thresh


def perspective_transform(img):
    """
    Execute perspective transform
    """
    # img = cv2.resize(img,(1280,720), interpolation=cv2.INTER_CUBIC)
    img_size = (img.shape[1], img.shape[0])

    src = np.float32(
        [[300, 1080],
         [1900, 800],
         [890, 500],
         [1290, 500]])
    dst = np.float32(
        [[300, 1080],
         [1900, 800],
         [300, 0],
         [1900, 0]])
    print(img_size)
    # plt.imshow(img, cmap='gray', vmin=0, vmax=1)
    # plt.show()
    m = cv2.getPerspectiveTransform(src, dst)
    m_inv = cv2.getPerspectiveTransform(dst, src)

    warped = cv2.warpPerspective(img, m, img_size, flags=cv2.INTER_LINEAR)
    # plt.imshow(warped, cmap='gray', vmin=0, vmax=1)
    # plt.show()
    unwarped = cv2.warpPerspective(warped, m_inv, (warped.shape[1], warped.shape[0]), flags=cv2.INTER_LINEAR)  # DEBUG

    return warped, unwarped, m, m_inv


if __name__ == '__main__':
    img_file = 'test_images/test5.jpg'

    with open('calibrate_camera.p', 'rb') as f:
        save_dict = pickle.load(f)
    mtx = save_dict['mtx']
    dist = save_dict['dist']

    img = mpimg.imread(img_file)
    img = cv2.undistort(img, mtx, dist, None, mtx)

    img, abs_bin, mag_bin, dir_bin, hls_bin = combined_thresh(img)

    warped, unwarped, m, m_inv = perspective_transform(img)

    plt.imshow(warped, cmap='gray', vmin=0, vmax=1)
    plt.show()

    plt.imshow(unwarped, cmap='gray', vmin=0, vmax=1)
    plt.show()
