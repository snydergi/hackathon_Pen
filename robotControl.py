from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
import math

waistMax = 180 * math.pi / 180
waistMin = -180 * math.pi / 180
shoulderMax = 107 * math.pi / 180
shoulderMin = -111 * math.pi / 180
elbowMax = 92 * math.pi / 180
elbowMin = -121 * math.pi / 180
wristMax = 123 * math.pi / 180
wristMin = -100 * math.pi / 180

def updateJointPositions():
    waistPos = robot.core.robot_get_single_joint_state('waist')['position']
    shoulderPos = robot.core.robot_get_single_joint_state('shoulder')['position']
    elbowPos = robot.core.robot_get_single_joint_state('elbow')['position']
    wristPos = robot.core.robot_get_single_joint_state('wrist_angle')['position']
    return waistPos, shoulderPos, elbowPos, wristPos

# The robot object is what you use to control the robot
robot = InterbotixManipulatorXS("px100", "arm", "gripper")

robot_startup()
mode = "h"

waistPos, shoulderPos, elbowPos, wristPos = updateJointPositions()

# Let the user select the position
while mode != 'q':
    mode=input("[h]ome, [s]leep, [o]pen grip, [c]lose grip, [r]otate waist, [e]lbow move, [w]rist move, [q]uit ")
    if mode == "h":
        robot.arm.go_to_home_pose()
        waistPos, shoulderPos, elbowPos, wristPos = updateJointPositions()
    elif mode == "s":
        robot.arm.go_to_sleep_pose()
        waistPos, shoulderPos, elbowPos, wristPos = updateJointPositions()
    elif mode == "c":
        robot.gripper.grasp()
    elif mode == "o":
        robot.gripper.release()
    elif mode == "r":
        printMsg = 'Current Position is: %f' % wristPos
        print(printMsg)
        waistChange = float(input("Input change in radians (-Pi to Pi): "))
        if waistPos + waistChange < waistMax and waistPos + waistChange > waistMin:
            robot.arm.set_single_joint_position('waist', waistPos+waistChange)
            waistPos += waistChange
    elif mode == "e":
        printMsg = 'Current Position is: %f' % elbowPos
        print(printMsg)
        elbowChange = float(input("Input change in radians (APPROX. -2.11 to 1.60): "))
        if elbowPos + elbowChange < elbowMax and elbowPos + elbowChange > elbowMin:
            robot.arm.set_single_joint_position('elbow', elbowPos+elbowChange)
            elbowPos += elbowChange
    elif mode == "w":
        print("Sorry not setup yet!")

robot_shutdown()