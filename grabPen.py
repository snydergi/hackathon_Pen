import scipy.sparse
import scipy.spatial
import realSense as rs
import robotControl as rc
import cv2
import scipy
import time

#Initialize transformation parameters from calibration
R_Matrix = [[ 0.99765557, -0.064186,    0.02373881],
            [-0.02169981,  0.03227973,  0.99924328],
            [-0.06490371, -0.99741575,  0.03081123]]
t_Vector = [ 0.20839625, -0.37753637,  0.13887384]
R = scipy.spatial.transform.Rotation.from_matrix(R_Matrix)

#Initialize camera and robot
mrGrip = rc.MrGrip()
camera = rs.RealSense(0)

while True:
    mrGrip.robot.gripper.release()
    #Capture Frame
    camera.getOneConvertedFrame()

    #If frame has a valid centroid
    if (camera.cx != 0 and camera.cy != 0):
        convertedPt = R.apply(camera.coordConverted) + t_Vector
        mrGrip.robot.arm.set_ee_pose_components(convertedPt[0],convertedPt[1],convertedPt[2])
        mrGrip.robot.arm.set_single_joint_position('wrist_angle', mrGrip.wristPos - 0.5)
        time.sleep(1)
        mrGrip.robot.gripper.grasp()
        time.sleep(4)

    cv2.imshow('Test Window', camera.contourImage)
    key = cv2.waitKey(2000)
    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

camera.cleanup()
mrGrip.robotShutdown()