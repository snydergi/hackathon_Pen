import scipy.spatial
import realSense as rs
import robotControl as rc
import time
import scipy

# cameraPointList = []
# robotPointList = []
# Rmat = []
# t = []

def runCalibration(mrGrip, cam):
    cameraPointList = []
    robotPointList = []
    Rmat = []
    t = []
    for pt in mrGrip.calibrationPoints:
        mrGrip.goToJointPositions(pt)
        eePose = mrGrip.robot.arm.get_ee_pose()
        eeXYZ = [eePose[0][-1],eePose[1][-1],eePose[2][-1]]
        robotPointList.append(eeXYZ)
        cam.getOneConvertedFrame()
        cameraPointList.append(cam.coordConverted)
        time.sleep(2)
    # cam.cleanup()
    # print(cameraPointList)
    # print(mrGrip.calibrationPoints)
    camX, camY, camZ = calcCentroidFromPtList(cameraPointList)
    robX, robY, robZ = calcCentroidFromPtList(robotPointList)
    cameraPointList = subtractCentroidFromPointlist(cameraPointList,camX,camY,camZ)
    robotPointList = subtractCentroidFromPointlist(robotPointList,robX,robY,robZ)
    Rmat, rssd = scipy.spatial.transform.Rotation.align_vectors(robotPointList, cameraPointList)
    print(Rmat.as_matrix())
    t = [robX,robY,robZ] - Rmat.apply([camX,camY,camZ])
    print(t)
    return Rmat, t

def calcCentroidFromPtList(pointList):
    cx = 0
    cy = 0
    cz = 0
    for pt in pointList:
       cx += pt[0] 
       cy += pt[1]
       cz += pt[2]
    cx = cx/len(pointList)
    cy = cy/len(pointList)
    cz = cz/len(pointList)
    return cx, cy, cz

def subtractCentroidFromPointlist(pointList,cx,cy,cz):
    for i in range(len(pointList)):
        pointList[i][0] -= cx
        pointList[i][1] -= cy
        pointList[i][2] -= cz
    return pointList

# mrGrip = rc.MrGrip()
# cam = rs.RealSense(0)
# runCalibration(mrGrip,cam)