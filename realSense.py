import pyrealsense2 as rs
import numpy as np
import cv2

class RealSense():

    def __init__(self,streamRecordPlay):
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))
        self.cx = 0
        self.cy = 0
        self.coordConverted = []
        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("This requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        if streamRecordPlay == 1:
            self.config.enable_record_to_file('testVideo')
        if streamRecordPlay == 2:
            self.config.enable_device_from_file('testVideo')
    
        self.profile = self.pipeline.start(self.config)

        self.clippingDistanceMeters = 1
        self.getDepthScale()
        self.clippingDistanceScaled = self.clippingDistanceMeters / self.depthScale

        self.alignSetup()
        
    def getDepthScale(self):
        self.depthSensor = self.profile.get_device().first_depth_sensor()
        self.depthScale = self.depthSensor.get_depth_scale()
        print("Depth Scale is: ", self.depthScale)       
    
    def alignSetup(self):
        alignTo = rs.stream.color
        self.align = rs.align(alignTo)

    def captureFrame(self):
        frames = self.pipeline.wait_for_frames()
        alignedFrames = self.align.process(frames)
        self.alignedDepthFrame = alignedFrames.get_depth_frame()
        self.colorFrame = alignedFrames.get_color_frame()
        if not self.alignedDepthFrame or not self.colorFrame:
            print("Depth or color frame invalid")

    def getDepthAndColorImage(self):
        self.depthImage = np.asanyarray(self.alignedDepthFrame.get_data())
        self.colorImage = np.asanyarray(self.colorFrame.get_data())
        self.removeBackground()

    def removeBackground(self):
        grey_color = 153
        self.depth_image_3d = np.dstack((self.depthImage,self.depthImage,self.depthImage)) #depth image is 1 channel, color is 3 channels
        self.bg_removed = np.where((self.depth_image_3d > self.clippingDistanceScaled) | (self.depth_image_3d <= 0), grey_color, self.colorImage)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depthImage, alpha=0.03), cv2.COLORMAP_JET)
        self.images = np.hstack((self.bg_removed, depth_colormap))

    def convertCoords(self, px, py):
        # cfg = self.pipeline.start(self.config)
        # profile = cfg.get_stream(rs.stream.color)
        prof2 = self.profile.get_stream(rs.stream.color)
        intr = prof2.as_video_stream_profile().get_intrinsics()
        coordConv = rs.rs2_deproject_pixel_to_point(intr, [px,py], self.depthImage[py][px] * self.depthScale)
        return coordConv

    def convertAndDrawCentroid(self, contour, contourImage):
        cnt = contour[0]
        for i in range(len(contour)):
            if cv2.contourArea(cnt) < cv2.contourArea(contour[i]):
                cnt = contour[i]
        M = cv2.moments(cnt)
        if(M['m00'] != 0):
            self.cx = int(M['m10']/M['m00'])
            self.cy = int(M['m01']/M['m00'])
            cv2.circle(contourImage,(self.cx,self.cy),2,(255,0,0),5)
            self.coordConverted = self.convertCoords(self.cx,self.cy)
            print(self.coordConverted)

    def getOneConvertedFrame(self):
        self.captureFrame()
        self.getDepthAndColorImage()
        self.removeBackground()
        colorChange = cv2.cvtColor(self.bg_removed, cv2.COLOR_BGR2HSV)
        maskedImage = cv2.inRange(colorChange,(113,40,0),(142,174,273))
        contour, hierarchy = cv2.findContours(maskedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contourImage = cv2.drawContours(self.colorImage,contour,-1,(0,0,255),3)
        if len(contour) >= 1:
            self.convertAndDrawCentroid(contour,contourImage)
        cv2.imshow('Test Window', contourImage)
        key = cv2.waitKey(2000)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()

    def cleanup(self):
        self.pipeline.stop()