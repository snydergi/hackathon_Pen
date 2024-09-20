import scipy.spatial
import realSense as rs
import robotControl as rc
import time
import scipy

mrGrip = rc.MrGrip()
cam = rs.RealSense(0)
cameraPointList = []
robotPointList = []
Rmat = []
t = []

def runCalibration():
    time.sleep(1)
    mrGrip.robot.gripper.release()
    time.sleep(1)
    mrGrip.robot.gripper.grasp()
    time.sleep(2)
    for pt in mrGrip.calibrationPoints:

        #Go to calibration points
        mrGrip.robot.arm.set_joint_positions(pt)
        time.sleep(2)

        #Create lists of end effector xyz @ calibration points
        robotPointList.append(mrGrip.getPoseXYZ())

        #Create one frame and add converted coordinate to cam point list
        cam.getOneConvertedFrame()
        cameraPointList.append(cam.coordConverted)

    print("Robot Points: ")
    print(robotPointList)
    print("Camera Points: ")
    print(cameraPointList)

    mrGrip.robotShutdown()
    cam.cleanup()

runCalibration()