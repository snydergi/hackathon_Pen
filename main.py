import realSense
import cv2

num = int(input("Enter 0 to just stream, 1 to record, or 2 to playback recording: "))
cam = realSense.RealSense(num)

try:
    while True:
        cam.captureFrame()
        cam.getDepthAndColorImage()
        cam.removeBackground()

        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', cam.images)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    cam.cleanup()