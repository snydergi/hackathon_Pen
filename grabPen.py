import robotControl as rc
import realSense as rs
import calibrate
import cv2
import time

mrGrip = rc.MrGrip()
cam = rs.RealSense(0)

# mrGrip.robot.gripper.release()
# time.sleep(2)
mrGrip.robot.gripper.grasp()
time.sleep(2)
R, t = calibrate.runCalibration(mrGrip, cam)
mrGrip.robot.gripper.release()

while True:
    cam.captureFrame()
    cam.getDepthAndColorImage()
    cam.removeBackground()
    colorChange = cv2.cvtColor(cam.bg_removed, cv2.COLOR_BGR2HSV)
    maskedImage = cv2.inRange(colorChange,(112,87,81),(143,163,255))
    contour, hierarchy = cv2.findContours(maskedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contourImage = cv2.drawContours(cam.colorImage,contour,-1,(0,0,255),3)
    if len(contour) >= 1:
        cam.convertAndDrawCentroid(contour,contourImage)
        eePt = R.apply(cam.coordConverted) + t
        # print("Pen Centroid: ")
        # print(cam.coordConverted)
        # print("EE Pt: ")
        # print(eePt)
        mrGrip.robot.arm.set_ee_pose_components(eePt[0],eePt[1],eePt[2])
        # time.sleep(2)
        # mrGrip.robot.gripper.grasp()
    cv2.imshow('Test Window', contourImage)
    key = cv2.waitKey(2000)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

cam.cleanup()
mrGrip.robotShutdown()
