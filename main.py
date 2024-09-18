import realSense
import cv2

num = int(input("Enter 0 to just stream, 1 to record, or 2 to playback recording: "))
cam = realSense.RealSense(num)

hue_slider_max = 179
sat_slider_max = 255
val_slider_max = 255
hue_slider_min = 179
sat_slider_min = 255
val_slider_min = 255

################## BEGIN_CITATION [2] ######################
def nothing(x):
    pass

cv2.namedWindow('Test Window')
cv2.createTrackbar('Hue Max', 'Test Window', 0, hue_slider_max, nothing)
cv2.createTrackbar('Hue Min', 'Test Window', 0, hue_slider_min, nothing)
cv2.createTrackbar('Sat Max', 'Test Window', 0, sat_slider_max, nothing)
cv2.createTrackbar('Sat Min', 'Test Window', 0, sat_slider_min, nothing)
cv2.createTrackbar('Val Max', 'Test Window', 0, val_slider_max, nothing)
cv2.createTrackbar('Val Min', 'Test Window', 0, val_slider_min, nothing)

while True:
    cam.captureFrame()
    cam.getDepthAndColorImage()
    cam.removeBackground()

    # cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
    # cv2.imshow('Align Example', cam.images)
    
    colorChange = cv2.cvtColor(cam.bg_removed, cv2.COLOR_BGR2HSV)

    #################### BEGIN CITATION [2] ###########################
    hmax = cv2.getTrackbarPos('Hue Max', 'Test Window')
    hmin = cv2.getTrackbarPos('Hue Min', 'Test Window')
    smax = cv2.getTrackbarPos('Sat Max', 'Test Window')
    smin = cv2.getTrackbarPos('Sat Min', 'Test Window')
    vmax = cv2.getTrackbarPos('Val Max', 'Test Window')
    vmin = cv2.getTrackbarPos('Val Min', 'Test Window')
    #################### END_CITATION [2] #############################

    #################### BEGIN_CITATION [3] ###########################
    colorChange[:, :, 0] = (colorChange[:, :, 0] - hmax)
    colorChange[:, :, 1] = (colorChange[:, :, 1] - smax)
    colorChange[:, :, 2] = (colorChange[:, :, 2] - vmax)
    #################### END_CITATION [3] #############################

    cv2.imshow('Test Window', colorChange)

    key = cv2.waitKey(1)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break
cam.cleanup()
