from interbotix_xs_modules.xs_robot.arm import InterbotixManipulatorXS
from interbotix_common_modules.common_robot.robot import robot_shutdown, robot_startup
import math

class MrGrip():

    def __init__(self):
        self.waistMax = 180 * math.pi / 180
        self.waistMin = -180 * math.pi / 180
        self.shoulderMax = 107 * math.pi / 180
        self.shoulderMin = -111 * math.pi / 180
        self.elbowMax = 92 * math.pi / 180
        self.elbowMin = -121 * math.pi / 180
        self.wristMax = 123 * math.pi / 180
        self.wristMin = -100 * math.pi / 180

        self.calibrationPt1 = [0.000, 0.030680, 0.069029, 0.033748]
        self.calibrationPt2 = [0.500, 0.030680, 0.069029, 0.033748]
        self.calibrationPt3 = [-0.500, 0.030680, 0.069029, 0.033748]
        self.calibrationPt4 = [-0.009204, 0.027612, -0.671767, 0.006136]
        self.calibrationPt5 = [-0.509204, 0.027612, 0.078233, 0.006136]

        self.calibrationPoints = [self.calibrationPt1, self.calibrationPt2, self.calibrationPt3, self.calibrationPt4, self.calibrationPt5]

        # The robot object is what you use to control the robot
        self.robot = InterbotixManipulatorXS("px100", "arm", "gripper")

        # robot_startup()
        self.mode = "h"

        self.waistPos, self.shoulderPos, self.elbowPos, self.wristPos = self.updateJointPositions()

    def updateJointPositions(self):
        waistPos = self.robot.core.robot_get_single_joint_state('waist')['position']
        shoulderPos = self.robot.core.robot_get_single_joint_state('shoulder')['position']
        elbowPos = self.robot.core.robot_get_single_joint_state('elbow')['position']
        wristPos = self.robot.core.robot_get_single_joint_state('wrist_angle')['position']
        return waistPos, shoulderPos, elbowPos, wristPos

    def manualControl(self):
        # Let the user select the position
        while self.mode != 'q':
            self.mode=input("[h]ome, [s]leep, [o]pen grip, [c]lose grip, [r]otate waist, [e]lbow move, [w]rist move, [p]rint current positions, [q]uit ")
            if self.mode == "h":
                self.robot.arm.go_to_home_pose()
                waistPos, shoulderPos, elbowPos, wristPos = self.updateJointPositions()
            elif self.mode == "s":
                self.robot.arm.go_to_sleep_pose()
                waistPos, shoulderPos, elbowPos, wristPos = self.updateJointPositions()
            elif self.mode == "c":
                self.robot.gripper.grasp()
            elif self.mode == "o":
                self.robot.gripper.release()
            elif self.mode == "r":
                printMsg = 'Current Position is: %f' % wristPos
                print(printMsg)
                waistChange = float(input("Input change in radians (-Pi to Pi): "))
                if waistPos + waistChange < self.waistMax and waistPos + waistChange > self.waistMin:
                    self.robot.arm.set_single_joint_position('waist', waistPos+waistChange)
                    waistPos += waistChange
            elif self.mode == "e":
                printMsg = 'Current Position is: %f' % elbowPos
                print(printMsg)
                elbowChange = float(input("Input change in radians (APPROX. -2.11 to 1.60): "))
                if elbowPos + elbowChange < self.elbowMax and elbowPos + elbowChange > self.elbowMin:
                    self.robot.arm.set_single_joint_position('elbow', elbowPos+elbowChange)
                    elbowPos += elbowChange
            elif self.mode == "w":
                print("Sorry not setup yet!")
            elif self.mode == "p":
                printMsg = 'Current Waist Position is: %f' % waistPos
                print(printMsg)
                printMsg = 'Current Shoulder Position is: %f' % shoulderPos
                print(printMsg)
                printMsg = 'Current Elbow Position is: %f' % elbowPos
                print(printMsg)
                printMsg = 'Current Wrist Position is: %f' % wristPos
                print(printMsg)

    def robotShutdown(self):
        robot_shutdown()

    def goToJointPositions(self, posList):
        self.robot.arm.set_joint_positions(posList)

# roobit = MrGrip()
# roobit.manualControl()
# roobit.goToJointPositions(roobit.calibrationPt1)
# roobit.robotShutdown()