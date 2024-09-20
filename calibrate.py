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
        mrGrip.robot.arm.set_joint_positions(pt)
        time.sleep(2)
    mrGrip.robotShutdown()

runCalibration()