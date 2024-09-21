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
        if(cam.cx != 0 and cam.cy != 0):
            cameraPointList.append(cam.coordConverted)

    # print("Robot Points: ")
    # print(robotPointList)
    # print("Camera Points: ")
    # print(cameraPointList)

    camCx,camCy,camCz = findCentroid(cameraPointList)
    robCx,robCy,robCz = findCentroid(robotPointList)

    cameraPointsLessCentroid = subtractCentroid(camCx,camCy,camCz,cameraPointList)
    robotPointsLessCentroid = subtractCentroid(robCx,robCy,robCz,robotPointList)

    R_Mat, rssd = scipy.spatial.transform.Rotation.align_vectors(robotPointsLessCentroid, cameraPointsLessCentroid)

    tVec = [robCx,robCy,robCz] - R_Mat.apply([camCx,camCy,camCz])

    transformedCameraPoints = transformPoints(R_Mat,tVec,cameraPointList)

    print("Robot Points: ")
    print(robotPointList)
    print("Transformed Camera Points: ")
    print(transformedCameraPoints)

    mrGrip.robotShutdown()
    cam.cleanup()

def findCentroid(pointList):
    x = 0
    y = 0
    z = 0
    for pt in pointList:
        x += pt[0]
        y += pt[1]
        z += pt[2]
    x = (x / len(pointList))
    y = (y / len(pointList))
    z = (z / len(pointList))
    return x,y,z

def subtractCentroid(x,y,z,pointList):
    newList = []
    for pt in pointList:
        xn = pt[0] - x
        yn = pt[1] - y
        zn = pt[2] - z
        newList.append([xn,yn,zn])
    return newList

def transformPoints(R,t,pointsList):
    newList = []
    for pt in pointsList:
        newPt = R.apply(pt) + t
        newList.append(newPt)
    return newList


runCalibration()