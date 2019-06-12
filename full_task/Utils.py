import rospy
from clever import srv
from std_srvs.srv import Trigger
from mavros_msgs.srv import CommandBool
import math
import time

led_colors = {"takeoff":Color(200,0,200), "wait":Color(0,90,140), "rec":Color(225,50,5), "land":Color(225,90,0)}

class Magnet:
    def __init__(self, pin=22):
        pi = pigpio.pi()
        self._pin = pin
        pi.set_mode(self._pin, pigpio.OUTPUT)
        # pi.write(self._pin, 0)
    def on(self):
        pi.write(self._pin, 1)
    def off(self):
        pi.write(self._pin, 0)

class Copter:
    def __init__(self, markers_flipped=False):
        rospy.init_node('flight')
        self.get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
        self.navigate = rospy.ServiceProxy('navigate', srv.Navigate)
        self.navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
        self.set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
        self.set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
        self.set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
        self.set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
        self.land = rospy.ServiceProxy('land', Trigger)
        self.arming = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)
        self.zero_z = 2
        self.markers_flipped = markers_flipped
        self.start_coord = (0, 0)
        # self.tolerance = 0.2
    def get_distance(self, x1, y1, z1, x2, y2, z2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    def zero_z(self):
        """
        Zero floor level
        """
        
        zz = 0
        for i in range(10):
            telem = self.get_telemetry(frame_id="aruco_map")
            zz += telem.z
            rospy.sleep(0.15)
        self.zero_z = zz/10
        

    def get_telemetry_aruco(self):
        telem =  self.get_telemetry(frame_id="aruco_map")
        if self.markers_flipped == True:
            telem.z = self.zero_z - telem.z
            return telem
        else:
            return telem

    def navigate_aruco(self, x=0, y=0, z=0, yaw=float('nan'), speed=0.5):
        if self.markers_flipped == True:
            return self.navigate(x=x, y=y, z=self.zero_z-z, yaw=yaw, speed=speed, frame_id='aruco_map')
        else:
            return telem

    def takeoff(self, z):
        self.navigate(z=z, speed=0.56, frame_id="body", auto_arm=True)
        rospy.sleep(1.8)
        self.navigate_aruco(x=start_coord[0], y=start_coord[1], z=z, speed=0.5)

    def go_to_point(self, point, yaw=float('nan'), speed=0.5, tolerance=0.2):
        self.navigate_aruco(x=point[0], y=point[1], z=point[2], yaw=yaw, speed=speed)
        
        while True:
            telem = self.get_telemetry(frame_id=frame_id)
            # Вычисляем расстояние до заданной точки
            if self.get_distance(x, y, z, telem.x, telem.y, telem.z) < tolerance:
                # Долетели до необходимой точки
                break
            rospy.sleep(0.2)
    def land(self):
        self.land()
        time.sleep(5)
        self.arming(False)

