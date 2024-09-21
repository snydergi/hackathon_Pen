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

        # self.calibrationPt1 = [0.000, 0.030680, 0.069029, 0.033748]
        # self.calibrationPt2 = [0.500, 0.030680, 0.069029, 0.033748]
        # self.calibrationPt3 = [-0.500, 0.030680, 0.069029, 0.033748]
        # self.calibrationPt4 = [-0.009204, 0.027612, -0.671767, 0.006136]
        # self.calibrationPt5 = [-0.509204, 0.027612, 0.078233, 0.006136]

        self.cp1 = [0.00,0.052155,0.075165,0.038350]
        self.cp2 = [0.25,0.052155,0.075165,0.038350]
        self.cp3 = [0.50,0.052155,0.075165,0.038350]
        self.cp4 = [-0.25,0.052155,0.075165,0.038350]
        self.cp5 = [-0.50,0.052155,0.075165,0.038350]
        self.cp6 = [0.00,0.052155,-0.424835,0.038350]
        self.cp7 = [0.25,0.052155,-0.424835,0.038350]
        self.cp8 = [0.50,0.052155,-0.424835,0.038350]
        self.cp9 = [-0.25,0.052155,-0.424835,0.038350]
        self.cp10 = [-0.50,0.052155,-0.424835,0.038350]

        self.calibrationPoints = [self.cp1, self.cp2, self.cp3, self.cp4, self.cp5, self.cp6, self.cp7, self.cp8, self.cp9, self.cp10]

        # The robot object is what you use to control the robot
        self.robot = InterbotixManipulatorXS("px100", "arm", "gripper")

        robot_startup()
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
                self.waistPos, self.shoulderPos, self.elbowPos, self.wristPos = self.updateJointPositions()
            elif self.mode == "s":
                self.robot.arm.go_to_sleep_pose()
                self.waistPos, self.shoulderPos, self.elbowPos, self.wristPos = self.updateJointPositions()
            elif self.mode == "c":
                self.robot.gripper.grasp()
            elif self.mode == "o":
                self.robot.gripper.release()
            elif self.mode == "r":
                printMsg = 'Current Position is: %f' % self.wristPos
                print(printMsg)
                waistChange = float(input("Input change in radians (-Pi to Pi): "))
                if self.waistPos + waistChange < self.waistMax and self.waistPos + waistChange > self.waistMin:
                    self.robot.arm.set_single_joint_position('waist', self.waistPos+waistChange)
                    self.waistPos += waistChange
            elif self.mode == "e":
                printMsg = 'Current Position is: %f' % self.elbowPos
                print(printMsg)
                elbowChange = float(input("Input change in radians (APPROX. -2.11 to 1.60): "))
                if self.elbowPos + elbowChange < self.elbowMax and self.elbowPos + elbowChange > self.elbowMin:
                    self.robot.arm.set_single_joint_position('elbow', self.elbowPos+elbowChange)
                    self.elbowPos += elbowChange
            elif self.mode == "w":
                print("Sorry not setup yet!")
            elif self.mode == "p":
                printMsg = 'Current Waist Position is: %f' % self.waistPos
                print(printMsg)
                printMsg = 'Current Shoulder Position is: %f' % self.shoulderPos
                print(printMsg)
                printMsg = 'Current Elbow Position is: %f' % self.elbowPos
                print(printMsg)
                printMsg = 'Current Wrist Position is: %f' % self.wristPos
                print(printMsg)

    def robotShutdown(self):
        robot_shutdown()

    def goToJointPositions(self, posList):
        self.robot.arm.set_joint_positions(posList)

    def getPoseXYZ(self):
        eePose = self.robot.arm.get_ee_pose()
        eex = eePose[0][3]
        eey = eePose[1][3]
        eez = eePose[2][3]
        return [eex,eey,eez]

# roobit = MrGrip()
# roobit.manualControl()
# roobit.robotShutdown()