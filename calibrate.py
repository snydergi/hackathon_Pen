import scipy.spatial
import realSense as rs
import robotControl as rc
import time
import scipy

# mrGrip = rc.MrGrip()
# cam = rs.RealSense(0)
cameraPointList = []
robotPointList = []
Rmat = []
t = []

def runCalibration(mrGrip, cam):
    for pt in mrGrip.calibrationPoints:
        mrGrip.goToJointPositions(pt)
        eePose = mrGrip.robot.arm.get_ee_pose()
        eeXYZ = [eePose[0][-1],eePose[1][-1],eePose[2][-1]]
        robotPointList.append(eeXYZ)
        cam.getOneConvertedFrame()
        cameraPointList.append(cam.convertCoords(cam.cx,cam.cy))
        time.sleep(2)
    # cam.cleanup()
    print(cameraPointList)
    print(mrGrip.calibrationPoints)
    Rmat, rssd = scipy.spatial.transform.Rotation.align_vectors(robotPointList, cameraPointList)
    print(Rmat.as_matrix())
    t = robotPointList[0] - Rmat.apply(cameraPointList[0])
    print(t)
    return Rmat, t


# runCalibration()