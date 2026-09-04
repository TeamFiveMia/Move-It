
import rclpy
from rcplpy.node import Node
from robot_kinematics import DiffDriveKinematics,MecanumKinematics,ThreeWheelOmniKinematics,FourWheelOmniKinematics
class WheelOdometryNode(Node):
    def __init__(self):
        super().__init__('wheel_odometry_node')
        # parameters
        self.declare_parameter('drive_type','DiffDriveKinematics')
        self.declare_parameter('track_width',0.2)
        self.declare_parameter('wheelbase',0.2)
        self.declare_parameter('wheel_radius',0.2)
        # x,y,yaw location of robot
        self.x = 0.0
        self.y = 0.0
        self.yaw=0.0
        # time
        self.time = self.get_clock().now()
        # get the parameters -> variales
        self.drive_type = self.get_parameter('drive_type').value
        self.track_width = self.get_parameter('track_width').value
        self.wheelbase = self.get_parameter('wheelbase').value
        self.wheel_radius = self.get_parameter('wheel_radius').value
        # check whick kinematics is used
        if self.drive_type == 'DiffDriveKinematics':
            self.kinematics = DiffDriveKinematics(self.track_width,self.wheel_radius)
        elif self.drive_type == 'MecanumKinematics':
            self.kinematics = MecanumKinematics(self.track_width,self.wheelbase,self.wheel_radius)
        elif self.drive_type == 'ThreeWheelOmniKinematics':
            self.kinematics = ThreeWheelOmniKinematics(self.track_width,self.wheelbase,self.wheel_radius)
        elif self.drive_type == 'FourWheelOmniKinematics':
            self.kinematics = FourWheelOmniKinematics(self.track_width,self.wheelbase,self.wheel_radius)
        else:
            self.get_logger().error('Wrong type')
        
